#version 330

struct Sphere
{
    vec3 position;
    float radius;
    vec3 color;
};

struct Box
{
    vec3 position;
    vec3 dimensions;
    vec3 color;
};

struct Light
{
    vec3 position;
    vec3 color;
};

const int LIGHTS = 2;
Light lights[LIGHTS];
const int SPHERES = 1;
Sphere spheres[SPHERES];
const int BOXES = 2;
Box boxes[BOXES];

in vec2 uv;
in vec2 Texcoord;

out lowp vec4 outColor;

const float PI = 3.14159f;
const float HIT_DIST = 0.1f;
const float EPSILON = 0.01f;
const float h = 0.0001f;

const int SPHERE = 1;
const int BOX    = 2;

uniform int MAX_STEPS = 64;
uniform float rayDist = 0.5f;
uniform float zNear = 0.5f;
uniform float zFar = 25f;
uniform vec3 cameraPos = vec3(0f);

float sdSphere(vec3 point, vec3 position, float radius)
{
    return length(point - position) - radius;
}

float udBox(vec3 point, vec3 position, vec3 dimensions)
{
    return length(max(abs(point - position) - dimensions/2f, 0.0));
}

float closestDistance(vec3 point, out vec3 color)
{
    float minimum = 3.4028e+38f;

    for (int i = 0; i < BOXES; i++)
    {
        Box box = boxes[i];
        float dist = udBox(point, box.position, box.dimensions);

        if (dist < minimum)
        {
            minimum = dist;
            color = box.color;
        }
    }

    for (int i = 0; i < SPHERES; i++)
    {
        Sphere sphere = spheres[i];
        float dist = sdSphere(point, sphere.position, sphere.radius);

        if (dist < minimum)
        {
            minimum = dist;
            color = sphere.color;
        }
    }

    return minimum;
}

float closestDistance(vec3 point)
{
    vec3 temp;
    return closestDistance(point, temp);
}

bool march(vec3 origin, vec3 direction, out vec3 hit, out vec3 color)
{
    float t = 0f;

    for (int i = 0; i < MAX_STEPS; i++)
    {
        hit = origin + direction * t;
        float closest = closestDistance(hit, color);

        if (closest <= EPSILON)
        {
            return true;
        }

        t += closest;

        if (t > zFar)
        {
            return false;
        }
    }

    return false;
}

vec3 getNormal(vec3 p)
{
	return normalize(
        vec3(
		    closestDistance(p + vec3(h, 0, 0)) -
            closestDistance(p - vec3(h, 0, 0)),
		    closestDistance(p + vec3(0, h, 0)) -
            closestDistance(p - vec3(0, h, 0)),
		    closestDistance(p + vec3(0, 0, h)) -
            closestDistance(p - vec3(0, 0, h))
        )
    );
}

vec3 getBackground(vec3 direction)
{
    return vec3(1f);
}

//http://lolengine.net/blog/2013/09/21/picking-orthogonal-vector-combing-coconuts
vec3 orthogonal(vec3 v)
{
    return abs(v.x) > abs(v.z) ? vec3(-v.y, v.x, 0.0) : vec3(0.0, -v.z, v.y);
}

float ambientOcclusion(vec3 p, vec3 n)
{
    float stepSize = 0.01f;
    float t = stepSize;
    float oc = 0.0f;

    for(int i = 0; i < 10; ++i)
    {
        float d = closestDistance(p + n * t);
        oc += t - d; // Actual distance to surface - distance field value
        t += stepSize;
    }

    return 1 - clamp(oc, 0, 1);
}

float checkVisibility(vec3 lightPos, vec3 hit, float k)
{
    vec3 direction = normalize(lightPos - hit);
    vec3 newOrigin = hit + direction*HIT_DIST;
    float res = 1f;
    float t = 0f;

    for (int j = 0; j < MAX_STEPS; j++)
    {
        float closest = closestDistance(newOrigin + direction*t);

        if (closest < EPSILON || t > zFar)
        {
            break;
        }

        res = min(res, k*closest/t);
        t += closest;
    }

    return min(res, 1f);
}

vec3 color(vec3 origin, vec3 direction)
{
    vec3 hit;
    vec3 color = vec3(0f);
    vec3 hitColor;

    for (int i = 0; i < LIGHTS; i++)
    {
        Light light = lights[i];

        if (march(origin, direction, hit, hitColor))
        {
            vec3 normal = getNormal(hit);
            float visibility = checkVisibility(light.position, hit, 2);

            if (visibility > 0.0)
            {
                vec3 lightDirection = normalize(light.position - hit);
                vec3 intensity = light.color * dot(normal, lightDirection);
                color += (hitColor * intensity) *
                    (visibility * ambientOcclusion(hit, normal));
                //color += ambientOcclusion(hit, normal) * vec3(1f);
            }
        }
    }

    return min(color/lights.length(), vec3(1f));
}

void setupScene()
{
    lights[0].position = vec3(-10, 10, 0);
    lights[0].color = vec3(1);
    lights[1].position = vec3(10, 0, 0);
    lights[1].color = vec3(1);

    boxes[0].position = vec3(0f, -3.5f, 10f);
    boxes[0].dimensions = vec3(20f, 1f, 20f);
    boxes[0].color = vec3(0.5f, 0.5f, 0f);

    boxes[1].position = vec3(6f, 0f, 10f);
    boxes[1].dimensions = vec3(6f);
    boxes[1].color = vec3(0.5f, 0.5f, 0f);

    spheres[0].position = vec3(0f, 0f, 10f);
    spheres[0].radius = 3f;
    spheres[0].color = vec3(0f, 0.5f, 0.5f);
}

void main()
{
    setupScene();

    vec3 direction = normalize(vec3(uv * rayDist, zNear));
    outColor = vec4(color(cameraPos, direction), 1);
}
