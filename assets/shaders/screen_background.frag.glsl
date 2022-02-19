#version 130

uniform sampler2D p3d_Texture0;
uniform float osg_FrameTime;
uniform int osg_FrameNumber;

uniform float pq_panning_rate_x;
uniform float pq_panning_rate_y;

in vec2 texcoord;
out vec4 p3d_FragColor;

void main() {
  float offsetX = osg_FrameTime * pq_panning_rate_x * 0.5;
  float offsetY = osg_FrameTime * pq_panning_rate_y * 0.5;
  vec2 pancoord = vec2(texcoord.x + offsetX, texcoord.y + offsetY); 

  vec4 texture = texture(p3d_Texture0, pancoord);
  p3d_FragColor = texture.rgba;
}