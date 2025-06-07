import unittest

import pygame
import pygame._render as _render


class DrawableObject:
    def __init__(self):
        self.drawn = False
        self.area = None
        self.dest = None

    def draw(self, area, dest):
        self.drawn = True
        self.area = area
        self.dest = dest


class RendererTest(unittest.TestCase):
    def setUp(self):
        self.window = pygame.Window(size=(100, 100))
        self.renderer = _render.Renderer(self.window)

    def test_to_surface(self):
        self.renderer.draw_color = "YELLOW"
        self.renderer.draw_point((10, 10))  # assumes Renderer.draw_point works
        surf1 = self.renderer.to_surface()
        self.assertEqual(surf1.get_at((10, 10)), pygame.Color(255, 255, 0, 255))
        self.assertEqual(surf1.size, (100, 100))

        surf2 = pygame.Surface((150, 150))
        self.renderer.to_surface(surf2)
        self.assertEqual(surf2.get_at((10, 10)), pygame.Color(255, 255, 0, 255))

        surf3 = self.renderer.to_surface(area=pygame.Rect(5, 5, 20, 20))
        self.assertEqual(surf3.get_at((5, 5)), pygame.Color(255, 255, 0, 255))
        self.assertEqual(surf3.size, (20, 20))

        surf4 = pygame.Surface((150, 150))
        self.renderer.to_surface(surf4, pygame.Rect(7, 7, 40, 40))
        self.assertEqual(surf4.get_at((3, 3)), pygame.Color(255, 255, 0, 255))

        small_surf = pygame.Surface((50, 50))
        with self.assertRaises(ValueError):
            self.renderer.to_surface(small_surf)

    def test_blit(self):
        texture = _render.Texture(self.renderer, (20, 20))
        image = _render.Image(texture)
        drawable_object = DrawableObject()
        dest = pygame.Rect(10, 10, 20, 20)
        area = pygame.Rect(0, 0, 15, 15)

        self.renderer.blit(
            texture, dest, area
        )  # TODO Assert after Texture implementation

        self.renderer.blit(image, dest, area)  # TODO Assert after Image implementation

        self.renderer.blit(drawable_object, dest, area)
        self.assertEqual(drawable_object.drawn, True)
        self.assertEqual(drawable_object.area, area)
        self.assertEqual(drawable_object.dest, dest)

    def test_clear(self):
        self.renderer.draw_color = "YELLOW"
        self.renderer.clear()
        surf = self.renderer.to_surface()
        for x in range(surf.width):
            for y in range(surf.height):
                self.assertEqual(surf.get_at((x, y)), pygame.Color(255, 255, 0, 255))

    def test_draw_point(self):
        self.renderer.draw_color = "YELLOW"
        self.renderer.draw_point((10, 10))
        surf = self.renderer.to_surface()
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x or y:
                    self.assertEqual(
                        surf.get_at((10 + x, 10 + y)), pygame.Color(0, 0, 0, 255)
                    )
                else:
                    self.assertEqual(
                        surf.get_at((10, 10)), pygame.Color(255, 255, 0, 255)
                    )

    def test_draw_line(self):
        self.renderer.draw_color = "YELLOW"
        self.renderer.draw_line((10, 10), (40, 40))
        surf = self.renderer.to_surface()
        test_points = ((10, 10), (20, 20), (30, 30), (40, 40))
        for point in test_points:
            self.assertEqual(surf.get_at(point), pygame.Color(255, 255, 0, 255))

    def test_draw_triangle(self):
        self.renderer.draw_color = "YELLOW"
        self.renderer.draw_triangle((10, 10), (10, 40), (40, 10))
        surf = self.renderer.to_surface()
        test_points = (
            (10, 10),
            (20, 10),
            (30, 10),
            (40, 10),
            (10, 20),
            (30, 20),
            (10, 30),
            (20, 30),
            (10, 40),
        )
        for point in test_points:
            self.assertEqual(surf.get_at(point), pygame.Color(255, 255, 0, 255))

    def test_draw_rect(self):
        self.renderer.draw_color = "YELLOW"
        self.renderer.draw_rect(pygame.Rect(10, 10, 11, 11))
        surf = self.renderer.to_surface()
        test_points = ((10, 15), (15, 10), (20, 15), (15, 20))
        for point in test_points:
            self.assertEqual(surf.get_at(point), pygame.Color(255, 255, 0, 255))

    def test_draw_quad(self):
        self.renderer.draw_color = "YELLOW"
        self.renderer.draw_quad((10, 40), (40, 10), (70, 40), (40, 70))
        surf = self.renderer.to_surface()
        test_points = ((30, 20), (50, 20), (30, 60), (50, 60))
        for point in test_points:
            self.assertEqual(surf.get_at(point), pygame.Color(255, 255, 0, 255))

    def test_fill_triangle(self):
        self.renderer.draw_color = "YELLOW"
        self.renderer.fill_triangle((10, 10), (10, 40), (40, 10))
        surf = self.renderer.to_surface()
        for x in range(10, 29):
            self.assertEqual(surf.get_at((x, 20)), pygame.Color(255, 255, 0, 255))
        for x in range(10, 19):
            self.assertEqual(surf.get_at((x, 30)), pygame.Color(255, 255, 0, 255))

    def test_fill_rect(self):
        self.renderer.draw_color = "YELLOW"
        self.renderer.fill_rect(pygame.Rect(10, 10, 11, 11))
        surf = self.renderer.to_surface()
        for x in range(10, 21):
            for y in range(10, 21):
                self.assertEqual(surf.get_at((x, y)), pygame.Color(255, 255, 0, 255))

    def test_fill_quad(self):
        self.renderer.draw_color = "GREEN"
        self.renderer.draw_quad((10, 40), (40, 10), (70, 40), (40, 70))
        self.renderer.draw_color = "YELLOW"
        self.renderer.fill_quad((10, 40), (40, 10), (70, 40), (40, 70))
        surf = self.renderer.to_surface()
        for x in range(30, 50):
            self.assertEqual(surf.get_at((x, 20)), pygame.Color(255, 255, 0, 255))
            self.assertEqual(surf.get_at((x, 59)), pygame.Color(255, 255, 0, 255))

    def test_viewport(self):
        self.assertEqual(self.renderer.get_viewport(), pygame.Rect(0, 0, 100, 100))
        self.renderer.set_viewport(pygame.Rect(20, 20, 60, 60))
        self.assertEqual(self.renderer.get_viewport(), pygame.Rect(20, 20, 60, 60))
        self.renderer.set_viewport(None)
        self.assertEqual(self.renderer.get_viewport(), pygame.Rect(0, 0, 100, 100))

    def test_logical_size(self):
        self.assertEqual(self.renderer.logical_size, (0, 0))
        self.renderer.logical_size = (10, 10)
        self.assertEqual(self.renderer.logical_size, (10, 10))

    def test_scale(self):
        self.assertEqual(self.renderer.scale, (1.0, 1.0))
        self.renderer.scale = (0.5, 2)
        self.assertEqual(self.renderer.scale, (0.5, 2.0))

    def test_target(self):
        self.assertEqual(self.renderer.target, None)
        texture = _render.Texture(self.renderer, (10, 10), target=True)
        self.renderer.target = texture
        self.assertEqual(id(self.renderer.target), id(texture))
        self.renderer.target = None
        self.assertEqual(self.renderer.target, None)

    @unittest.skip("Unable to create that blend_mode on all devices")
    def test_compose_custom_blend_mode(self):
        color_mode, alpha_mode = (
            (
                pygame.BLENDFACTOR_SRC_COLOR,
                pygame.BLENDFACTOR_ONE_MINUS_DST_COLOR,
                pygame.BLENDOPERATION_MAXIMUM,
            ),
            (
                pygame.BLENDFACTOR_ONE_MINUS_SRC_ALPHA,
                pygame.BLENDFACTOR_DST_ALPHA,
                pygame.BLENDOPERATION_MINIMUM,
            ),
        )
        custom_blend_mode = self.renderer.compose_custom_blend_mode(
            color_mode, alpha_mode
        )
        self.assertEqual(custom_blend_mode, 157550645)
        self.renderer.draw_blend_mode = custom_blend_mode
        self.assertEqual(self.renderer.draw_blend_mode, custom_blend_mode)

    def test_draw_blend_mode(self):
        self.assertEqual(self.renderer.draw_blend_mode, pygame.BLENDMODE_NONE)
        self.renderer.draw_blend_mode = pygame.BLENDMODE_MUL
        self.assertEqual(self.renderer.draw_blend_mode, pygame.BLENDMODE_MUL)
        unsupported_blend_mode = pygame.BLENDMODE_MUL + 1
        with self.assertRaises(Exception):
            self.renderer.draw_blend_mode = unsupported_blend_mode

    def test_draw_color(self):
        self.assertEqual(self.renderer.draw_color, pygame.Color(0, 0, 0, 0))
        self.renderer.draw_color = "YELLOW"
        self.assertEqual(self.renderer.draw_color, pygame.Color(255, 255, 0, 255))
