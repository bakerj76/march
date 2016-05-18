#version 330

in vec2 Texcoord;

out lowp vec4 outColor;

uniform sampler2D tex;

void main()
{
    outColor = texture(tex, Texcoord);
}
