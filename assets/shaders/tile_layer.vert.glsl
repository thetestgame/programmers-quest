/*
 * Copyright (C) Nxt Games 2021
 * All Rights Reserved
 *
 * Written by Jordan Maxwell <jordan.maxwell@nxt-games.com>, January 7th, 2021
 *
 * NXT GAMES CONFIDENTAL
 * _______________________
 *
 * NOTICE:  All information contained herein is, and remains
 * the property of Nxt Games and its suppliers,
 * if any. The intellectual and technical concepts contained
 * herein are proprietary to Nxt Games
 * and its suppliers and may be covered by U.S. and Foreign Patents,
 * patents in process, and are protected by trade secret or copyright law.
 * Dissemination of this information or reproduction of this material
 * is strictly forbidden unless prior written permission is obtained
 * from Nxt Games.
*/

#version 130

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

in vec2 frct_tilePosition;
in vec2 frct_tileCount;
in float frct_tileSheet;

// Output to fragment shader
out vec2 texcoord;
out vec2 tilePosition;
out vec2 tileCount;
out float tileSheet;

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;

  texcoord = p3d_MultiTexCoord0;
  tilePosition = frct_tilePosition;
  tileCount = frct_tileCount;
  tileSheet = frct_tileSheet;
}