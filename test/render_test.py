import gc
import unittest
import weakref

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
        surface = pygame.Surface((10, 10))
        surface.fill((80, 120, 160, 200))
        texture = _render.Texture.from_surface(self.renderer, surface)
        image = _render.Image(texture)
        drawable_object = DrawableObject()
        dest = pygame.Rect(10, 10, 20, 20)
        area = pygame.Rect(0, 0, 15, 15)

        self.renderer.blit(texture, dest, area)
        result = self.renderer.to_surface()
        self.assertEqual(pygame.Color(0, 0, 0, 255), result.get_at((9, 20)))
        for x in range(10, 30):
            self.assertEqual(pygame.Color(80, 120, 160, 255), result.get_at((x, 20)))
        self.assertEqual(pygame.Color(0, 0, 0, 255), result.get_at((30, 20)))
        self.renderer.clear()

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

    def test_logical_window_mapping(self):
        self.renderer.logical_size = (10, 10)
        self.assertEqual(self.renderer.coordinates_to_window((10, 10)), (100, 100))
        self.assertEqual(self.renderer.coordinates_from_window((100, 100)), (10, 10))
        with self.assertRaises(TypeError):
            self.renderer.coordinates_to_window(42, 42)
        with self.assertRaises(TypeError):
            self.renderer.coordinates_from_window(42, 42)

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


class TextureTest(unittest.TestCase):
    def setUp(self):
        self.window = pygame.Window(size=(100, 100))
        self.renderer = _render.Renderer(self.window)
        self.texture = _render.Texture(self.renderer, (80, 60))

    def create_texture_from_surface(self):
        surface = pygame.Surface((100, 100))
        surface.fill(pygame.Color(80, 120, 160, 128))
        return _render.Texture.from_surface(self.renderer, surface)

    def test_init(self):
        _render.Texture(self.renderer, (100, 100))
        _render.Texture(self.renderer, (100, 100), depth=32)
        with self.assertRaises(ValueError):
            _render.Texture(self.renderer, (100, 100), depth=33)
        _render.Texture(self.renderer, (100, 100), depth=32, static=True)
        _render.Texture(self.renderer, (100, 100), depth=32, streaming=True)
        _render.Texture(self.renderer, (100, 100), depth=32, target=True)
        with self.assertRaises(ValueError):
            _render.Texture(
                self.renderer, (100, 100), depth=32, static=True, target=True
            )
        with self.assertRaises(ValueError):
            _render.Texture(
                self.renderer, (100, 100), depth=32, target=True, streaming=True
            )
        with self.assertRaises(ValueError):
            _render.Texture(
                self.renderer, (100, 100), depth=32, static=True, streaming=True
            )

    def test_alpha(self):
        self.assertEqual(255, self.texture.alpha)
        self.texture.alpha = 128
        self.assertEqual(128, self.texture.alpha)

    def test_blend_mode(self):
        self.assertEqual(pygame.BLENDMODE_NONE, self.texture.blend_mode)
        self.texture.blend_mode = pygame.BLENDMODE_BLEND
        self.assertEqual(pygame.BLENDMODE_BLEND, self.texture.blend_mode)

    def test_color(self):
        self.assertEqual(pygame.Color(255, 255, 255, 255), self.texture.color)
        self.texture.color = pygame.Color(100, 110, 120, 130)
        self.assertEqual(pygame.Color(100, 110, 120, 255), self.texture.color)

    def test_width(self):
        self.assertEqual(80, self.texture.width)
        with self.assertRaises(AttributeError):
            self.texture.width = 100

    def test_height(self):
        self.assertEqual(60, self.texture.height)
        with self.assertRaises(AttributeError):
            self.texture.height = 100

    def test_renderer(self):
        self.assertEqual(self.renderer, self.texture.renderer)
        window2 = pygame.Window(size=(128, 128))
        renderer2 = _render.Renderer(window2)
        with self.assertRaises(AttributeError):
            self.texture.renderer = renderer2

    def test_get_rect(self):
        self.assertEqual(pygame.Rect(0, 0, 80, 60), self.texture.get_rect())
        self.assertEqual(
            pygame.Rect(10, 20, 80, 60), self.texture.get_rect(center=(50, 50))
        )

    def test_from_surface(self):
        surf_size = (50, 40)
        surface = pygame.Surface(surf_size)
        texture2 = _render.Texture.from_surface(self.renderer, surface)
        self.assertEqual(surf_size, (texture2.width, texture2.height))

    def test_draw_triangle(self):
        texture2 = self.create_texture_from_surface()
        texture2.draw_triangle(
            (50, 10),
            (10, 90),
            (90, 90),
            (0.5, 0.5),
            (0.8, 0.2),
            (1, 1),
            (100, 100, 100, 100),
            (80, 60, 40, 20),
            (150, 170, 190, 210),
        )
        result = self.renderer.to_surface()
        expected = [
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (28, 38, 45),
            (29, 39, 46),
            (29, 39, 47),
            (29, 40, 48),
            (29, 41, 49),
            (30, 41, 50),
            (30, 42, 52),
            (30, 43, 53),
            (31, 43, 54),
            (31, 44, 55),
            (31, 44, 56),
            (31, 45, 57),
            (32, 46, 59),
            (32, 46, 60),
            (32, 47, 61),
            (32, 48, 62),
            (33, 48, 63),
            (33, 49, 65),
            (33, 50, 66),
            (34, 50, 67),
            (34, 51, 68),
            (34, 52, 69),
            (34, 52, 70),
            (35, 53, 72),
            (35, 54, 73),
            (35, 54, 74),
            (35, 55, 75),
            (36, 55, 76),
            (36, 56, 78),
            (36, 57, 79),
            (37, 57, 80),
            (37, 58, 81),
            (37, 59, 82),
            (37, 59, 83),
            (38, 60, 85),
            (38, 61, 86),
            (38, 61, 87),
            (39, 62, 88),
            (39, 63, 89),
            (39, 63, 90),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ]
        start = 25
        for x in range(start, start + len(expected)):
            value = result.get_at((x, 50))
            for color_index in range(3):
                expected_value = expected[x - start][color_index]
                self.assertTrue(
                    expected_value - 1 <= value[color_index] <= expected_value + 1
                )

    def test_draw_quad(self):
        texture2 = self.create_texture_from_surface()
        texture2.draw_quad(
            (10, 10),
            (90, 10),
            (90, 90),
            (10, 90),
            (0.5, 0.5),
            (0.8, 0.2),
            (0.2, 0.8),
            (0.9, 0.9),
            (100, 100, 100, 100),
            (80, 60, 40, 20),
            (150, 170, 190, 210),
            (128, 128, 128, 128),
        )
        result = self.renderer.to_surface()
        expected = [
            (37, 58, 79),
            (37, 58, 80),
            (37, 58, 80),
            (37, 58, 81),
            (37, 59, 81),
            (38, 59, 82),
            (38, 59, 82),
            (38, 59, 83),
            (38, 60, 83),
            (38, 60, 84),
            (38, 60, 84),
            (38, 60, 84),
            (38, 61, 85),
            (38, 61, 85),
            (38, 61, 86),
            (38, 61, 86),
            (39, 62, 87),
            (39, 62, 87),
            (39, 62, 88),
            (39, 62, 88),
            (39, 62, 89),
            (39, 63, 89),
            (39, 63, 90),
            (39, 63, 90),
            (39, 63, 91),
            (39, 64, 91),
            (39, 63, 91),
            (39, 63, 90),
            (39, 63, 90),
            (39, 63, 89),
            (39, 63, 89),
            (39, 62, 88),
            (39, 62, 88),
            (39, 62, 88),
            (39, 62, 87),
            (38, 61, 87),
            (38, 61, 86),
            (38, 61, 86),
            (38, 61, 85),
            (38, 60, 85),
            (38, 60, 84),
            (38, 60, 84),
            (38, 60, 83),
            (38, 59, 83),
            (38, 59, 82),
            (38, 59, 82),
            (38, 59, 81),
            (38, 59, 81),
            (37, 58, 80),
            (37, 58, 80),
        ]
        start = 25
        for x in range(start, start + len(expected)):
            value = result.get_at((x, 50))
            for color_index in range(3):
                expected_value = expected[x - start][color_index]
                self.assertTrue(
                    expected_value - 1 <= value[color_index] <= expected_value + 1
                )

    def test_draw(self):
        texture2 = self.create_texture_from_surface()
        texture2.draw(pygame.Rect(10, 20, 40, 40), pygame.Rect(50, 30, 35, 20), 45)
        result = self.renderer.to_surface()
        for x in range(64, 82):
            self.assertEqual(pygame.Color(80, 120, 160, 255), result.get_at((x, 50)))

    def test_garbage_collection(self):
        reference = weakref.ref(self.texture)
        self.assertTrue(reference() is self.texture)
        del self.texture
        gc.collect()
        self.assertIsNone(reference())

    def test_update(self):
        surface = pygame.Surface((100, 100))
        surface.fill(pygame.Color(80, 120, 160, 128))
        self.texture.update(surface, pygame.Rect(10, 10, 80, 80))
        self.texture.draw()
        result = self.renderer.to_surface()
        for x in range(25, 75):
            self.assertEqual(pygame.Color(80, 120, 160, 255), result.get_at((x, 50)))

class ImageTest(unittest.TestCase):
    def setUp(self):
        '''self.window = pygame.Window(size=(100, 100))
        self.renderer = _render.Renderer(self.window)
        self.surface = pygame.Surface((50, 50))
        self.surface.fill(pygame.Color(80, 120, 160, 255))
        self.texture = _render.Texture.from_surface(self.renderer, self.surface)
        self.image = _render.Image(self.texture)'''

    def test_init_with_texture(self):
        """Test Image initialization with a Texture"""
        image = _render.Image(self.texture)
        self.assertEqual(image.texture, self.texture)
        self.assertEqual(image.srcrect, pygame.Rect(0, 0, 50, 50))
        self.assertEqual(image.alpha, 255.0)
        self.assertEqual(image.angle, 0.0)
        self.assertEqual(image.color, pygame.Color(255, 255, 255, 255))
        self.assertEqual(image.blend_mode, 0)
        self.assertEqual(image.flip_x, False)
        self.assertEqual(image.flip_y, False)
        self.assertEqual(image.origin, None)

    def test_init_with_image(self):
        """Test Image initialization with another Image"""
        image1 = _render.Image(self.texture, pygame.Rect(10, 10, 30, 30))
        image2 = _render.Image(image1)
        self.assertEqual(image2.texture, self.texture)
        self.assertEqual(image2.srcrect, pygame.Rect(10, 10, 30, 30))

    def test_init_with_srcrect(self):
        """Test Image initialization with a custom srcrect"""
        srcrect = pygame.Rect(10, 10, 30, 30)
        image = _render.Image(self.texture, srcrect)
        self.assertEqual(image.srcrect, pygame.Rect(10, 10, 30, 30))

    def test_alpha_property(self):
        """Test alpha property getter and setter"""
        self.assertEqual(self.image.alpha, 255.0)

        self.image.alpha = 128.5
        self.assertEqual(self.image.alpha, 128.5)

        self.image.alpha = 0
        self.assertEqual(self.image.alpha, 0.0)

        # Test invalid alpha values (should not raise error but may clamp)
        self.image.alpha = -10
        self.image.alpha = 300

    def test_angle_property(self):
        """Test angle property getter and setter"""
        self.assertEqual(self.image.angle, 0.0)

        self.image.angle = 45.5
        self.assertEqual(self.image.angle, 45.5)

        self.image.angle = -90
        self.assertEqual(self.image.angle, -90.0)

    def test_blend_mode_property(self):
        """Test blend_mode property getter and setter"""
        self.assertEqual(self.image.blend_mode, 0)

        self.image.blend_mode = 1
        self.assertEqual(self.image.blend_mode, 1)

    def test_color_property(self):
        """Test color property getter and setter"""
        self.assertEqual(self.image.color, pygame.Color(255, 255, 255, 255))

        self.image.color = (255, 0, 0)
        self.assertEqual(self.image.color, pygame.Color(255, 0, 0, 255))

        self.image.color = pygame.Color(0, 255, 0, 128)
        self.assertEqual(self.image.color, pygame.Color(0, 255, 0, 255))

    def test_flip_properties(self):
        """Test flip_x and flip_y properties"""
        self.assertEqual(self.image.flip_x, False)
        self.assertEqual(self.image.flip_y, False)

        self.image.flip_x = True
        self.assertEqual(self.image.flip_x, True)

        self.image.flip_y = True
        self.assertEqual(self.image.flip_y, True)

        self.image.flip_x = False
        self.assertEqual(self.image.flip_x, False)

    def test_origin_property(self):
        """Test origin property getter and setter"""
        self.assertEqual(self.image.origin, None)

        self.image.origin = (25.0, 25.0)
        self.assertEqual(self.image.origin, (25.0, 25.0))

        self.image.origin = None
        self.assertEqual(self.image.origin, None)

    def test_srcrect_property(self):
        """Test srcrect property getter and setter"""
        self.assertEqual(self.image.srcrect, pygame.Rect(0, 0, 50, 50))

        new_rect = pygame.Rect(10, 10, 30, 30)
        self.image.srcrect = new_rect
        self.assertEqual(self.image.srcrect, new_rect)

    def test_texture_property(self):
        """Test texture property getter and setter"""
        self.assertEqual(self.image.texture, self.texture)

        # Create another texture
        new_surface = pygame.Surface((30, 30))
        new_texture = _render.Texture.from_surface(self.renderer, new_surface)

        self.image.texture = new_texture
        self.assertEqual(self.image.texture, new_texture)

    def test_get_rect(self):
        """Test get_rect method"""
        rect = self.image.get_rect()
        self.assertEqual(rect, pygame.Rect(0, 0, 50, 50))

        # Test with custom srcrect
        self.image.srcrect = pygame.Rect(10, 10, 30, 30)
        rect = self.image.get_rect()
        self.assertEqual(rect, pygame.Rect(10, 10, 30, 30))

    def test_draw_method(self):
        """Test draw method"""
        # Basic draw should not raise an error
        self.image.draw()

        # Draw with parameters
        self.image.draw(
            srcrect=pygame.Rect(0, 0, 25, 25), dstrect=pygame.Rect(10, 10, 25, 25)
        )

        # Test the actual rendering result
        self.renderer.clear()
        self.image.draw(dstrect=pygame.Rect(20, 20, 50, 50))
        result = self.renderer.to_surface()
        # The center of the drawn image should have the expected color
        self.assertEqual(result.get_at((45, 45)), pygame.Color(80, 120, 160, 255))

    def test_draw_with_transformations(self):
        """Test draw with various transformations"""
        # Test with alpha
        self.image.alpha = 128
        self.image.draw()

        # Test with rotation
        self.image.angle = 45
        self.image.draw()

        # Test with flipping
        self.image.flip_x = True
        self.image.flip_y = True
        self.image.draw()

        # Test with origin
        self.image.origin = (25, 25)
        self.image.draw()

        # Test with color modulation
        self.image.color = (255, 0, 0)
        self.image.draw()

    def test_invalid_init_params(self):
        """Test Image initialization with invalid parameters"""
        with self.assertRaises(AttributeError):
            _render.Image("invalid")

        with self.assertRaises(TypeError):
            _render.Image(self.texture, "invalid_rect")

    def test_property_type_errors(self):
        """Test property setters with invalid types"""
        with self.assertRaises(TypeError):
            self.image.alpha = "invalid"

        with self.assertRaises(TypeError):
            self.image.angle = "invalid"

        with self.assertRaises(TypeError):
            self.image.blend_mode = "invalid"

        # Boolean properties accept any value and use truthiness
        # This is expected Python behavior, not an error
        self.image.flip_x = "invalid"  # Should be truthy
        self.assertTrue(self.image.flip_x)

        self.image.flip_y = 0  # Should be falsy
        self.assertFalse(self.image.flip_y)

        with self.assertRaises(TypeError):
            self.image.origin = "invalid"

        with self.assertRaises(TypeError):
            self.image.srcrect = "invalid"

        with self.assertRaises(TypeError):
            self.image.texture = "invalid"
