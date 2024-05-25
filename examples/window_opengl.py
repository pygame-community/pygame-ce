"""pygame.examples.window_opengl

Slightly modified version of the example at https://github.com/szabolcsdombi/zengl/blob/main/examples/pygame/hello_world.py
Modified to use Window API instead of the display module

Posted here with permission from https://github.com/szabolcsdombi given in the PGC discord server
"""

import pygame
import zengl

window_size = (1280, 720)

pygame.init()
window = pygame.Window(size=window_size, opengl=True)

ctx = zengl.context()

image = ctx.image(window_size, "rgba8unorm", samples=4)

pipeline = ctx.pipeline(
    vertex_shader="""
        #version 330 core

        out vec3 v_color;

        vec2 vertices[3] = vec2[](
            vec2(0.0, 0.8),
            vec2(-0.6, -0.8),
            vec2(0.6, -0.8)
        );

        vec3 colors[3] = vec3[](
            vec3(1.0, 0.0, 0.0),
            vec3(0.0, 1.0, 0.0),
            vec3(0.0, 0.0, 1.0)
        );

        void main() {
            gl_Position = vec4(vertices[gl_VertexID], 0.0, 1.0);
            v_color = colors[gl_VertexID];
        }
    """,
    fragment_shader="""
        #version 330 core

        in vec3 v_color;

        layout (location = 0) out vec4 out_color;

        void main() {
            out_color = vec4(v_color, 1.0);
            out_color.rgb = pow(out_color.rgb, vec3(1.0 / 2.2));
        }
    """,
    framebuffer=[image],
    topology="triangles",
    vertex_count=3,
)

clock = pygame.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    ctx.new_frame()
    image.clear()
    pipeline.render()
    image.blit()
    ctx.end_frame()

    window.flip()
    clock.tick(60)
