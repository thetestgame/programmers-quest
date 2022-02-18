#version 130
#extension GL_EXT_texture_array : enable

uniform sampler2DArray p3d_Texture0; // Tile Sheets used by this layer

// Input from vertex shader
in vec2 texcoord;
in vec2 tilePosition;
in vec2 tileCount;
in float tileSheet;

// Output from the fragment shader
out vec4 p3d_FragColor;

void main() {
  
  // Calculate our base tile image/frame
  vec2 tileScale = vec2(1.0) / tileCount;
  vec3 tilecoord = vec3(
      (texcoord.x + tilePosition.x) * tileScale.x,
      (texcoord.y * tileScale.y) + tilePosition.y * tileScale.y,
      tileSheet);

  vec4 tileColor = texture2DArray(p3d_Texture0, tilecoord);
  p3d_FragColor = tileColor.rgba;
}
