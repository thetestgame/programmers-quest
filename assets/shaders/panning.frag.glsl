#version 130

uniform sampler2D p3d_Texture0;
uniform float osg_FrameTime;
uniform int osg_FrameNumber;

in vec2 texcoord;
out vec4 p3d_FragColor;

void main() {
  float rate = 0.08;

  float offsetX = osg_FrameTime * rate;
  float offsetY = osg_FrameTime * rate;
  vec2 pancoord = vec2(texcoord.x + offsetX, texcoord.y - offsetY); 

  vec4 texture = texture(p3d_Texture0, pancoord * 5);
  p3d_FragColor = texture.rgba;
}