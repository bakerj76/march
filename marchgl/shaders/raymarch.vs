#version 330

in vec2 position;
in vec2 texcoord;

out vec2 uv;
out vec2 Texcoord;

void main()
{
    Texcoord = texcoord;
    uv = position;
    gl_Position = vec4(position, 0.0, 1.0);
}
