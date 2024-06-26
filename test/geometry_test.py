import math
import unittest
from math import sqrt

from pygame import Vector2, Vector3, Rect, FRect
from pygame.geometry import Circle


def float_range(a, b, step):
    result = []
    current_value = a
    while current_value < b:
        result.append(current_value)
        current_value += step
    return result


class CircleTypeTest(unittest.TestCase):
    def testConstruction_invalid_type(self):
        """Checks whether passing wrong types to the constructor
        raises the appropriate errors
        """
        invalid_types = (None, [], "1", (1,), [1, 2, 3], Vector2(1, 1))

        # Test x
        for value in invalid_types:
            with self.assertRaises(TypeError):
                c = Circle(value, 0, 1)
        # Test y
        for value in invalid_types:
            with self.assertRaises(TypeError):
                c = Circle(0, value, 1)
        # Test r
        for value in invalid_types + (-1,):
            with self.assertRaises(TypeError):
                c = Circle(0, 0, value)

    def test2ndConstruction_invalid_type(self):
        """Checks whether passing wrong types to the 2nd constructor
        raises the appropriate errors
        """
        invalid_types = (None, [], "1", (1,), [1, 2, 3], Vector2(1, 1))

        # Test x
        for value in invalid_types:
            with self.assertRaises(TypeError):
                c = Circle((value, 0), 1)
        # Test y
        for value in invalid_types:
            with self.assertRaises(TypeError):
                c = Circle((0, value), 1)
        # Test r
        for value in invalid_types + (-1,):
            with self.assertRaises(TypeError):
                c = Circle((0, 0), value)

    def testConstruction_invalid_arguments_number(self):
        """Checks whether passing the wrong number of arguments to the constructor
        raises the appropriate errors
        """
        arguments = (
            (1,),  # one non vec3 non circle arg
            (1, 1, 1, 1),  # four args
        )

        for arg_seq in arguments:
            with self.assertRaises(TypeError):
                c = Circle(*arg_seq)

    def testConstructionXYR_float(self):
        c = Circle(1.0, 2.0, 3.0)

        self.assertEqual(1.0, c.x)
        self.assertEqual(2.0, c.y)
        self.assertEqual(3.0, c.r)

    def testConstructionTUP_XYR_float(self):
        c = Circle((1.0, 2.0, 3.0))

        self.assertEqual(1.0, c.x)
        self.assertEqual(2.0, c.y)
        self.assertEqual(3.0, c.r)

    def testConstructionXYR_int(self):
        c = Circle(1, 2, 3)

        self.assertEqual(1.0, c.x)
        self.assertEqual(2.0, c.y)
        self.assertEqual(3.0, c.r)

    def testConstructionTUP_XYR_int(self):
        c = Circle((1, 2, 3))

        self.assertEqual(1.0, c.x)
        self.assertEqual(2.0, c.y)
        self.assertEqual(3.0, c.r)

    def testConstruction_zero_radius(self):
        c = Circle(1, 2, 0)

        self.assertEqual(1.0, c.x)
        self.assertEqual(2.0, c.y)
        self.assertEqual(0, c.r)

    def test_x(self):
        """Ensures changing the x attribute moves the circle and does not change
        the circle's radius.
        """
        expected_x = 10.0
        expected_y = 2.0
        expected_radius = 5.0
        c = Circle(1, expected_y, expected_radius)

        c.x = expected_x

        self.assertEqual(c.x, expected_x)
        self.assertEqual(c.y, expected_y)
        self.assertEqual(c.r, expected_radius)

    def test_x__invalid_value(self):
        """Ensures the x attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.x = value

    def test_x__del(self):
        """Ensures the x attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.x

    def test_y(self):
        """Ensures changing the y attribute moves the circle and does not change
        the circle's radius.
        """
        expected_x = 10.0
        expected_y = 2.0
        expected_radius = 5.0
        c = Circle(expected_x, 1, expected_radius)

        c.y = expected_y

        self.assertEqual(c.x, expected_x)
        self.assertEqual(c.y, expected_y)
        self.assertEqual(c.r, expected_radius)

    def test_y__invalid_value(self):
        """Ensures the y attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.y = value

    def test_y__del(self):
        """Ensures the y attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.y

    def test_r(self):
        """Ensures changing the r attribute changes the radius without moving the circle."""
        expected_x = 10.0
        expected_y = 2.0
        expected_radius = 5.0
        c = Circle(expected_x, expected_y, 1.0)

        c.r = expected_radius

        self.assertEqual(c.x, expected_x)
        self.assertEqual(c.y, expected_y)
        self.assertEqual(c.r, expected_radius)

        c.radius = expected_radius
        self.assertEqual(c.x, expected_x)
        self.assertEqual(c.y, expected_y)
        self.assertEqual(c.radius, expected_radius)

    def test_r__invalid_value(self):
        """Ensures the r attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.r = value
            with self.assertRaises(TypeError):
                c.radius = value

        for value in (-10.3234, -1):
            with self.assertRaises(ValueError):
                c.r = value
            with self.assertRaises(ValueError):
                c.radius = value

    def test_r__del(self):
        """Ensures the r attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.r

        with self.assertRaises(AttributeError):
            del c.radius

    def test_r_sqr(self):
        """Ensures setting the r_sqr attribute matches the r_sqr passed"""
        expected_r_sqr = 10.0
        c = Circle(1.0, 1.0, 1.0)
        c.r_sqr = expected_r_sqr

        self.assertAlmostEqual(c.r_sqr, expected_r_sqr, places=14)

    def test_r_to_r_sqr(self):
        """Ensures changing the r attribute correctly changes the r_sqr attribute."""
        expected_r_sqr = 1.0
        expected_r_sqr2 = 100.0

        c = Circle(0, 0, 23)
        c2 = Circle(0, 0, 4)

        c.r = 1
        self.assertEqual(c.r_sqr, expected_r_sqr)

        c2.r = 10
        self.assertEqual(c2.r_sqr, expected_r_sqr2)

    def test_r_sqr_to_r(self):
        """Ensures changing the r_sqr attribute correctly changes the r attribute."""
        expected_r = 2.0

        c = Circle(0, 0, 23)

        c.r_sqr = 4.0
        self.assertEqual(c.r, expected_r)
        self.assertEqual(c.radius, expected_r)

        c.r_sqr = 13.33421
        self.assertEqual(c.r, sqrt(13.33421))
        self.assertEqual(c.radius, sqrt(13.33421))

    def test_r_sqr__invalid_set(self):
        """Ensures the r_sqr attribute can't be set"""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.r_sqr = value

    def test_r_sqr__del(self):
        """Ensures the r attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.r

    def test_center(self):
        """Ensures changing the center moves the circle and does not change
        the circle's radius.
        """
        expected_x = 10.3
        expected_y = 2.12
        expected_radius = 5.0
        c = Circle(1, 1, expected_radius)

        c.center = (expected_x, expected_y)

        self.assertEqual(c.x, expected_x)
        self.assertEqual(c.y, expected_y)
        self.assertEqual(c.r, expected_radius)

    def test_center_update(self):
        """Ensures changing the x or y value of the circle correctly updates the center."""
        expected_x = 10.3
        expected_y = 2.12
        expected_radius = 5.0
        c = Circle(1, 1, expected_radius)

        c.x = expected_x
        self.assertEqual(c.center, (expected_x, c.y))

        c.y = expected_y
        self.assertEqual(c.center, (c.x, expected_y))

    def test_center_invalid_value(self):
        """Ensures the center attribute handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.center = value

    def test_center_del(self):
        """Ensures the center attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.center

    def test_area(self):
        """Ensures the area is calculated correctly."""
        c = Circle(0, 0, 1)

        self.assertEqual(c.area, math.pi)

    def test_area_update(self):
        """Ensures the area is updated correctly."""
        c = Circle(0, 0, 1)

        c.r = 2
        self.assertEqual(c.area, math.pi * 4)

        c.r_sqr = 100
        self.assertEqual(c.area, math.pi * (10**2))

    def test_area_invalid_value(self):
        """Ensures the area handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.area = value

        for value in (-10.3234, -1):
            with self.assertRaises(ValueError):
                c.area = value

    def test_area_del(self):
        """Ensures the area attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.area

    def test_circumference(self):
        """Ensures the circumference is calculated correctly."""
        c = Circle(0, 0, 1)

        self.assertEqual(c.circumference, math.tau)

    def test_circumference_update(self):
        """Ensures the circumference is updated correctly."""
        c = Circle(0, 0, 1)

        c.r = 2
        self.assertEqual(c.circumference, math.tau * 2)

        c.r_sqr = 100
        self.assertEqual(c.circumference, math.tau * 10)

    def test_circumference_invalid_value(self):
        """Ensures the circumference handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.circumference = value

        for value in (-10.3234, -1):
            with self.assertRaises(ValueError):
                c.circumference = value

    def test_circumference_del(self):
        """Ensures the circumference attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.circumference

    def test_diameter(self):
        """Ensures the diameter is calculated correctly."""
        c = Circle(0, 0, 1)

        self.assertEqual(c.diameter, 2.0)
        self.assertEqual(c.d, 2.0)

    def test_diameter_update(self):
        """Ensures the diameter is updated correctly."""
        c = Circle(0, 0, 1)

        c.r = 2
        self.assertEqual(c.diameter, 4.0)
        self.assertEqual(c.d, 4.0)

        c.r_sqr = 100
        self.assertEqual(c.diameter, 20.0)
        self.assertEqual(c.d, 20.0)

    def test_diameter_invalid_value(self):
        """Ensures the diameter handles invalid values correctly."""
        c = Circle(0, 0, 1)

        for value in (None, [], "1", (1,), [1, 2, 3]):
            with self.assertRaises(TypeError):
                c.diameter = value

        for value in (-10.3234, -1):
            with self.assertRaises(ValueError):
                c.diameter = value
            with self.assertRaises(ValueError):
                c.d = value

    def test_diameter_del(self):
        """Ensures the diameter attribute can't be deleted."""
        c = Circle(0, 0, 1)

        with self.assertRaises(AttributeError):
            del c.diameter

        with self.assertRaises(AttributeError):
            del c.d

    def test__str__(self):
        """Checks whether the __str__ method works correctly."""
        c_str = "<Circle((10.3, 3.2), 4.3)>"
        circle = Circle((10.3, 3.2), 4.3)
        self.assertEqual(str(circle), c_str)
        self.assertEqual(circle.__str__(), c_str)

    def test__repr__(self):
        """Checks whether the __repr__ method works correctly."""
        c_repr = "<Circle((10.3, 3.2), 4.3)>"
        circle = Circle((10.3, 3.2), 4.3)
        self.assertEqual(repr(circle), c_repr)
        self.assertEqual(circle.__repr__(), c_repr)

    def test_copy(self):
        c = Circle(10, 10, 4)
        # check 1 arg passed
        with self.assertRaises(TypeError):
            c.copy(10)

        # check copied circle has the same attribute values
        c_2 = c.copy()
        self.assertEqual(c.x, c_2.x)
        self.assertEqual(c.y, c_2.y)
        self.assertEqual(c.r, c_2.r)

        # check c2 is not c
        self.assertIsNot(c_2, c)

    def test_collidepoint_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 1), 1)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.collidepoint(value)

    def test_collidepoint_argnum(self):
        c = Circle(10, 10, 4)
        args = [tuple(range(x)) for x in range(3, 13)]

        # no params
        with self.assertRaises(TypeError):
            c.collidepoint()

        # too many params
        for arg in args:
            with self.assertRaises(TypeError):
                c.collidepoint(*arg)

    def test_collidepoint(self):
        c = Circle(0, 0, 5)

        p1 = (3, 3)
        p2 = (10, 10)
        p3 = Vector2(3, 3)
        p4 = Vector2(10, 10)

        # colliding single
        self.assertTrue(c.collidepoint(p1), "Expected True, point should collide here")
        self.assertTrue(c.collidepoint(p3), "Expected True, point should collide here")

        # not colliding single
        self.assertFalse(
            c.collidepoint(p2), "Expected False, point should not collide here"
        )
        self.assertFalse(
            c.collidepoint(p4), "Expected False, point should not collide here"
        )

        # colliding 2 args
        self.assertTrue(
            c.collidepoint(3, 3), "Expected True, point should collide here"
        )

        # not colliding 2 args
        self.assertFalse(
            c.collidepoint(10, 10), "Expected False, point should not collide here"
        )

    def test_collidecircle_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector2(1, 1), 1)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.collidecircle(value)

    def test_collidecircle_argnum(self):
        c = Circle(10, 10, 4)
        # no params
        with self.assertRaises(TypeError):
            c.collidecircle()

        with self.assertRaises(TypeError):
            c.collidecircle(Circle(10, 10, 4), Circle(10, 10, 4))

    def test_collidecircle(self):
        c = Circle(0, 0, 5)
        c_same = c.copy()
        c2 = Circle(10, 0, 5)
        c3 = Circle(100, 100, 5)
        c4 = Circle(10, 0, 4.999999999999)
        c5 = Circle(0, 0, 2)

        c6 = Circle(10, 0, 7)

        # touching
        self.assertTrue(
            c.collidecircle(c2), "Expected True, circles should collide here"
        )

        # partly colliding
        self.assertTrue(
            c.collidecircle(c6), "Expected True, circles should collide here"
        )

        # self colliding
        self.assertTrue(
            c.collidecircle(c), "Expected True, circles should collide with self"
        )

        # completely colliding
        self.assertTrue(
            c.collidecircle(c_same), "Expected True, circles should collide with self"
        )

        # not touching
        self.assertFalse(
            c.collidecircle(c3), "Expected False, circles should not collide here"
        )

        # barely not touching
        self.assertFalse(
            c.collidecircle(c4), "Expected False, circles should not collide here"
        )

        # small circle inside big circle
        self.assertTrue(
            c.collidecircle(c5), "Expected True, circles should collide here"
        )

        # big circle outside small circle
        self.assertTrue(
            c5.collidecircle(c), "Expected False, circles should collide here"
        )

    def test_colliderect_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 1), 1, True, False)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.colliderect(value)

    def test_colliderect_argnum(self):
        """tests if the function correctly handles incorrect number of parameters"""
        c = Circle(10, 10, 4)
        args = [(1), (1, 1), (1, 1, 1), (1, 1, 1, 1, 1)]
        # no params
        with self.assertRaises(TypeError):
            c.colliderect()

        # invalid num
        for arg in args:
            with self.assertRaises(TypeError):
                c.colliderect(*arg)

    def test_colliderect(self):
        """ensures the function correctly detects collisions with rects"""

        msgt = "Expected True, rect should collide here"
        msgf = "Expected False, rect should not collide here"
        # ====================================================
        c = Circle(0, 0, 5)

        r1, r2, r3 = Rect(2, 2, 4, 4), Rect(10, 15, 43, 24), Rect(0, 5, 4, 4)
        fr1, fr2, fr3 = FRect(r1), FRect(r2), FRect(r3)

        # colliding single
        for r in (r1, fr1):
            self.assertTrue(c.colliderect(r), msgt)

        # not colliding single
        for r in (r2, fr2):
            self.assertFalse(c.colliderect(r), msgf)

        # barely colliding single
        for r in (r3, fr3):
            self.assertTrue(c.colliderect(r), msgt)

        # colliding 4 args
        self.assertTrue(c.colliderect(2, 2, 4, 4), msgt)

        # not colliding 4 args
        self.assertFalse(c.colliderect(10, 15, 43, 24), msgf)

        # barely colliding single
        self.assertTrue(c.colliderect(0, 4.9999999999999, 4, 4), msgt)

        # ensure FRects aren't truncated
        c2 = Circle(0, 0, 0.35)
        c3 = Circle(2, 0, 0.65)
        fr9 = FRect(0.4, 0.0, 1, 1)
        self.assertFalse(c2.colliderect(fr9), msgf)
        self.assertFalse(c2.colliderect(0.4, 0.0, 1, 1), msgf)
        self.assertFalse(c2.colliderect((0.4, 0.0), (1, 1)), msgf)

        self.assertTrue(c3.colliderect(fr9), msgt)
        self.assertTrue(c3.colliderect(0.4, 0.0, 1, 1), msgt)
        self.assertTrue(c3.colliderect((0.4, 0.0), (1, 1)), msgt)

    def test_collideswith_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 1), 1)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.collideswith(value)

    def test_collideswith_argnum(self):
        c = Circle(10, 10, 4)
        args = [tuple(range(x)) for x in range(2, 4)]

        # no params
        with self.assertRaises(TypeError):
            c.collideswith()

        # too many params
        for arg in args:
            with self.assertRaises(TypeError):
                c.collideswith(*arg)

    def test_collideswith(self):
        """Ensures the collideswith function correctly registers collisions with circles, lines, rects and points"""
        c = Circle(0, 0, 5)

        # circle
        c2 = Circle(0, 10, 15)
        c3 = Circle(100, 100, 1)
        self.assertTrue(c.collideswith(c2))
        self.assertFalse(c.collideswith(c3))

        # rect
        r = Rect(0, 0, 10, 10)
        r2 = Rect(50, 0, 10, 10)
        self.assertTrue(c.collideswith(r))
        self.assertFalse(c.collideswith(r2))

        # rect
        r = FRect(0, 0, 10, 10)
        r2 = FRect(50, 0, 10, 10)
        self.assertTrue(c.collideswith(r))
        self.assertFalse(c.collideswith(r2))

        # point
        p = (0, 0)
        p2 = (50, 0)
        self.assertTrue(c.collideswith(p))
        self.assertFalse(c.collideswith(p2))

    def test_update(self):
        """Ensures that updating the circle position
        and dimension correctly updates position and dimension"""
        c = Circle(0, 0, 10)

        c.update(5, 5, 3)

        self.assertEqual(c.x, 5.0)
        self.assertEqual(c.y, 5.0)
        self.assertEqual(c.r, 3.0)
        self.assertEqual(c.r_sqr, 9.0)

    def test_update_argtype(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector2(1, 1), 1, 0.2324)

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.update(value)

    def test_update_argnum(self):
        c = Circle(10, 10, 4)

        # no params
        with self.assertRaises(TypeError):
            c.update()

        # too many params
        with self.assertRaises(TypeError):
            c.update(1, 1, 1, 1)

    def test_update_twice(self):
        """Ensures that updating the circle position
        and dimension correctly updates position and dimension"""
        c = Circle(0, 0, 10)

        c.update(5, 5, 3)
        c.update(0, 0, 10)

        self.assertEqual(c.x, 0.0)
        self.assertEqual(c.y, 0.0)
        self.assertEqual(c.r, 10)
        self.assertEqual(c.r_sqr, 100)

    def test_update_inplace(self):
        """Ensures that updating the circle to its position doesn't
        move the circle to another position"""
        c = Circle(0, 0, 10)
        centerx = c.x
        centery = c.y
        c_r = c.r
        c_r_sqr = c.r_sqr

        c.update(0, 0, 10)

        self.assertEqual(c.x, centerx)
        self.assertEqual(c.y, centery)
        self.assertEqual(c.r, c_r)
        self.assertEqual(c.r_sqr, c_r_sqr)

        c.update(c)

    def test_selfupdate(self):
        """Ensures that updating the circle to its position doesn't
        move the circle to another position"""
        c = Circle(0, 0, 10)
        centerx = c.x
        centery = c.y
        c_r = c.r
        c_r_sqr = c.r_sqr

        c.update(c)

        self.assertEqual(c.x, centerx)
        self.assertEqual(c.y, centery)
        self.assertEqual(c.r, c_r)
        self.assertEqual(c.r_sqr, c_r_sqr)

    def test_as_rect_invalid_args(self):
        c = Circle(0, 0, 10)

        invalid_args = [None, [], "1", (1,), Vector2(1, 1), 1]

        with self.assertRaises(TypeError):
            for arg in invalid_args:
                c.as_rect(arg)

    def test_as_rect(self):
        c = Circle(0, 0, 10)
        self.assertEqual(c.as_rect(), Rect(-10, -10, 20, 20))

    def test_as_frect_invalid_args(self):
        c = Circle(0, 0, 10)

        invalid_args = [None, [], "1", (1,), Vector2(1, 1), 1]

        with self.assertRaises(TypeError):
            for arg in invalid_args:
                c.as_frect(arg)

    def test_as_frect(self):
        c = Circle(0, 0, 10)
        self.assertEqual(c.as_frect(), FRect(-10, -10, 20, 20))

    def test_circle_richcompare(self):
        """Ensures that the circle correctly compares itself to other circles"""
        c = Circle(0, 0, 10)
        c2 = Circle(0, 0, 10)
        c3 = Circle(0, 0, 5)
        c4 = Circle(0, 0, 20)

        self.assertTrue(c == c2)
        self.assertFalse(c != c2)

        self.assertFalse(c == c3)
        self.assertTrue(c != c3)

        self.assertFalse(c == c4)
        self.assertTrue(c != c4)

        # self compare
        self.assertTrue(c == c)
        self.assertFalse(c != c)

        # not implemented compare
        with self.assertRaises(TypeError):
            c > c2
        with self.assertRaises(TypeError):
            c < c2
        with self.assertRaises(TypeError):
            c >= c2
        with self.assertRaises(TypeError):
            c <= c2

        # invalid types
        invalid_types = (
            None,
            [],
            "1",
            (1,),
            Vector2(1, 1),
            1,
            0.2324,
            Rect(0, 0, 10, 10),
            True,
        )

        for value in invalid_types:
            self.assertFalse(c == value)
            self.assertTrue(c != value)
            with self.assertRaises(TypeError):
                c > value
            with self.assertRaises(TypeError):
                c < value
            with self.assertRaises(TypeError):
                c >= value
            with self.assertRaises(TypeError):
                c <= value

    def test_move_invalid_args(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 3), Circle(3, 3, 1))

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.move(value)

    def test_move_argnum(self):
        c = Circle(10, 10, 4)

        invalid_args = [(1, 1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                c.move(*arg)

    def test_move_return_type(self):
        c = Circle(10, 10, 4)

        class CircleSub(Circle):
            pass

        cs = CircleSub(10, 10, 4)

        self.assertIsInstance(c.move(1, 1), Circle)
        self.assertIsInstance(cs.move(1, 1), CircleSub)

    def test_move(self):
        """Ensures that moving the circle position correctly updates position"""
        c = Circle(0, 0, 3)

        new_c = c.move(5, 5)

        self.assertEqual(new_c.x, 5.0)
        self.assertEqual(new_c.y, 5.0)
        self.assertEqual(new_c.r, 3.0)
        self.assertEqual(new_c.r_sqr, 9.0)

        new_c = new_c.move(-5, -10)

        self.assertEqual(new_c.x, 0.0)
        self.assertEqual(new_c.y, -5.0)

    def test_move_inplace(self):
        """Ensures that moving the circle position by 0, 0 doesn't move the circle"""
        c = Circle(1, 1, 3)

        c.move(0, 0)

        self.assertEqual(c.x, 1.0)
        self.assertEqual(c.y, 1.0)
        self.assertEqual(c.r, 3.0)
        self.assertEqual(c.r_sqr, 9.0)

    def test_move_equality(self):
        """Ensures that moving the circle by 0, 0 will
        return a circle that's equal to the original"""
        c = Circle(1, 1, 3)

        new_c = c.move(0, 0)

        self.assertEqual(new_c, c)

    def test_move_ip_invalid_args(self):
        """tests if the function correctly handles incorrect types as parameters"""
        invalid_types = (None, [], "1", (1,), Vector3(1, 1, 3), Circle(3, 3, 1))

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.move_ip(value)

    def test_move_ip_argnum(self):
        """tests if the function correctly handles incorrect number of args"""
        c = Circle(10, 10, 4)

        invalid_args = [(1, 1, 1), (1, 1, 1, 1)]

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                c.move_ip(*arg)

    def test_move_ip(self):
        """Ensures that moving the circle position correctly updates position"""
        c = Circle(0, 0, 3)

        c.move_ip(5, 5)

        self.assertEqual(c.x, 5.0)
        self.assertEqual(c.y, 5.0)
        self.assertEqual(c.r, 3.0)
        self.assertEqual(c.r_sqr, 9.0)

        c.move_ip(-5, -10)
        self.assertEqual(c.x, 0.0)
        self.assertEqual(c.y, -5.0)

    def test_move_ip_inplace(self):
        """Ensures that moving the circle position by 0, 0 doesn't move the circle"""
        c = Circle(1, 1, 3)

        c.move_ip(0, 0)

        self.assertEqual(c.x, 1.0)
        self.assertEqual(c.y, 1.0)
        self.assertEqual(c.r, 3.0)
        self.assertEqual(c.r_sqr, 9.0)

    def test_move_ip_equality(self):
        """Ensures that moving the circle by 0, 0 will
        return a circle that's equal to the original"""
        c = Circle(1, 1, 3)

        c.move_ip(0, 0)

        self.assertEqual(c, Circle(1, 1, 3))

    def test_move_ip_return_type(self):
        """Ensures that the move_ip method returns None"""
        c = Circle(10, 10, 4)

        class CircleSub(Circle):
            pass

        cs = CircleSub(10, 10, 4)

        self.assertEqual(type(c.move_ip(1, 1)), type(None))
        self.assertEqual(type(cs.move_ip(1, 1)), type(None))

    def test_meth_rotate_ip_invalid_argnum(self):
        """Ensures that the rotate_ip method correctly deals with invalid numbers of arguments."""
        c = Circle(0, 0, 1)

        with self.assertRaises(TypeError):
            c.rotate_ip()

        invalid_args = [
            (1, (2, 2), 2),
            (1, (2, 2), 2, 2),
            (1, (2, 2), 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2, 2, 2),
        ]

        for args in invalid_args:
            with self.assertRaises(TypeError):
                c.rotate_ip(*args)

    def test_meth_rotate_ip_invalid_argtype(self):
        """Ensures that the rotate_ip method correctly deals with invalid argument types."""
        c = Circle(0, 0, 1)

        invalid_args = [
            ("a",),  # angle str
            (None,),  # angle str
            ((1, 2)),  # angle tuple
            ([1, 2]),  # angle list
            (1, "a"),  # origin str
            (1, None),  # origin None
            (1, True),  # origin True
            (1, False),  # origin False
            (1, (1, 2, 3)),  # origin tuple
            (1, [1, 2, 3]),  # origin list
            (1, (1, "a")),  # origin str
            (1, ("a", 1)),  # origin str
            (1, (1, None)),  # origin None
            (1, (None, 1)),  # origin None
            (1, (1, (1, 2))),  # origin tuple
            (1, (1, [1, 2])),  # origin list
        ]

        for value in invalid_args:
            with self.assertRaises(TypeError):
                c.rotate_ip(*value)

    def test_meth_rotate_ip_return(self):
        """Ensures that the rotate_ip method always returns None."""
        c = Circle(0, 0, 1)

        for angle in float_range(-360, 360, 1):
            self.assertIsNone(c.rotate_ip(angle))
            self.assertIsInstance(c.rotate_ip(angle), type(None))

    def test_meth_rotate_invalid_argnum(self):
        """Ensures that the rotate method correctly deals with invalid numbers of arguments."""
        c = Circle(0, 0, 1)

        with self.assertRaises(TypeError):
            c.rotate()

        invalid_args = [
            (1, (2, 2), 2),
            (1, (2, 2), 2, 2),
            (1, (2, 2), 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2, 2),
            (1, (2, 2), 2, 2, 2, 2, 2, 2),
        ]

        for args in invalid_args:
            with self.assertRaises(TypeError):
                c.rotate(*args)

    def test_meth_rotate_invalid_argtype(self):
        """Ensures that the rotate method correctly deals with invalid argument types."""
        c = Circle(0, 0, 1)

        invalid_args = [
            ("a",),  # angle str
            (None,),  # angle str
            ((1, 2)),  # angle tuple
            ([1, 2]),  # angle list
            (1, "a"),  # origin str
            (1, None),  # origin None
            (1, True),  # origin True
            (1, False),  # origin False
            (1, (1, 2, 3)),  # origin tuple
            (1, [1, 2, 3]),  # origin list
            (1, (1, "a")),  # origin str
            (1, ("a", 1)),  # origin str
            (1, (1, None)),  # origin None
            (1, (None, 1)),  # origin None
            (1, (1, (1, 2))),  # origin tuple
            (1, (1, [1, 2])),  # origin list
        ]

        for value in invalid_args:
            with self.assertRaises(TypeError):
                c.rotate(*value)

    def test_meth_rotate_return(self):
        """Ensures that the rotate method always returns a Circle."""
        c = Circle(0, 0, 1)

        class CircleSubclass(Circle):
            pass

        cs = CircleSubclass(0, 0, 1)

        for angle in float_range(-360, 360, 1):
            self.assertIsInstance(c.rotate(angle), Circle)
            self.assertIsInstance(cs.rotate(angle), CircleSubclass)

    def test_meth_rotate(self):
        """Ensures the Circle.rotate() method rotates the Circle correctly."""

        def rotate_circle(circle: Circle, angle, center):
            def rotate_point(x, y, rang, cx, cy):
                x -= cx
                y -= cy
                x_new = x * math.cos(rang) - y * math.sin(rang)
                y_new = x * math.sin(rang) + y * math.cos(rang)
                return x_new + cx, y_new + cy

            angle = math.radians(angle)
            cx, cy = center if center is not None else circle.center
            x, y = rotate_point(circle.x, circle.y, angle, cx, cy)
            return Circle(x, y, circle.r)

        def assert_approx_equal(circle1, circle2, eps=1e-12):
            self.assertAlmostEqual(circle1.x, circle2.x, delta=eps)
            self.assertAlmostEqual(circle1.y, circle2.y, delta=eps)
            self.assertAlmostEqual(circle1.r, circle2.r, delta=eps)

        c = Circle(0, 0, 1)
        angles = float_range(-360, 360, 0.5)
        centers = [(a, b) for a in range(-10, 10) for b in range(-10, 10)]
        for angle in angles:
            assert_approx_equal(c.rotate(angle), rotate_circle(c, angle, None))
            for center in centers:
                assert_approx_equal(
                    c.rotate(angle, center), rotate_circle(c, angle, center)
                )

    def test_meth_rotate_ip(self):
        """Ensures the Circle.rotate_ip() method rotates the Circle correctly."""

        def rotate_circle(circle: Circle, angle, center):
            def rotate_point(x, y, rang, cx, cy):
                x -= cx
                y -= cy
                x_new = x * math.cos(rang) - y * math.sin(rang)
                y_new = x * math.sin(rang) + y * math.cos(rang)
                return x_new + cx, y_new + cy

            angle = math.radians(angle)
            cx, cy = center if center is not None else circle.center
            x, y = rotate_point(circle.x, circle.y, angle, cx, cy)
            circle.x = x
            circle.y = y
            return circle

        def assert_approx_equal(circle1, circle2, eps=1e-12):
            self.assertAlmostEqual(circle1.x, circle2.x, delta=eps)
            self.assertAlmostEqual(circle1.y, circle2.y, delta=eps)
            self.assertAlmostEqual(circle1.r, circle2.r, delta=eps)

        c = Circle(0, 0, 1)
        angles = float_range(-360, 360, 0.5)
        centers = [(a, b) for a in range(-10, 10) for b in range(-10, 10)]
        for angle in angles:
            c.rotate_ip(angle)
            assert_approx_equal(c, rotate_circle(c, angle, None))
            for center in centers:
                c.rotate_ip(angle, center)
                assert_approx_equal(c, rotate_circle(c, angle, center))

    def test_contains_argtype(self):
        """Tests if the function correctly handles incorrect types as parameters"""

        invalid_types = (None, [], "1", (1,), 1, (1, 2, 3))

        c = Circle(10, 10, 4)

        for value in invalid_types:
            with self.assertRaises(TypeError):
                c.contains(value)

    def test_contains_argnum(self):
        """Tests if the function correctly handles incorrect number of parameters"""
        c = Circle(10, 10, 4)

        invalid_args = [(Circle(10, 10, 4), Circle(10, 10, 4))]

        with self.assertRaises(TypeError):
            c.contains()

        for arg in invalid_args:
            with self.assertRaises(TypeError):
                c.contains(*arg)

    def test_contains_return_type(self):
        """Tests if the function returns the correct type"""
        c = Circle(10, 10, 4)
        items = [
            Circle(3, 4, 15),
            (0, 0),
            Vector2(0, 0),
            Rect(0, 0, 10, 10),
            FRect(0, 0, 10, 10),
        ]

        for item in items:
            self.assertIsInstance(c.contains(item), bool)

    def test_contains_circle(self):
        """Ensures that the contains method correctly determines if a circle is
        contained within the circle"""
        c = Circle(10, 10, 4)
        c2 = Circle(10, 10, 2)
        c3 = Circle(100, 100, 5)
        c4 = Circle(16, 10, 7)

        # self
        self.assertTrue(c.contains(c))

        # self-like
        c_s = Circle(c)
        self.assertTrue(c.contains(c_s))

        # contained circle
        self.assertTrue(c.contains(c2))

        # not contained circle
        self.assertFalse(c.contains(c3))

        # intersecting circle
        self.assertFalse(c.contains(c4))

        # bigger circle not contained in smaller circle
        self.assertFalse(c2.contains(c))
        self.assertFalse(c3.contains(c4))

    def test_contains_point(self):
        """Ensures that the contains method correctly determines if a point is
        contained within the circle"""
        c = Circle(10, 10, 4)
        p1 = (10, 10)
        p2 = (10, 15)
        p3 = (100, 100)
        p4 = (c.x + math.sin(math.pi / 4) * c.r, c.y + math.cos(math.pi / 4) * c.r)

        p1v = Vector2(p1)
        p2v = Vector2(p2)
        p3v = Vector2(p3)
        p4v = Vector2(p4)

        # contained point
        self.assertTrue(c.contains(p1))

        # not contained point
        self.assertFalse(c.contains(p2))
        self.assertFalse(c.contains(p3))

        # on the edge
        self.assertTrue(c.contains(p4))

        # contained point
        self.assertTrue(c.contains(p1v))

        # not contained point
        self.assertFalse(c.contains(p2v))
        self.assertFalse(c.contains(p3v))

        # on the edge
        self.assertTrue(c.contains(p4v))

    def test_contains_rect_frect(self):
        """Ensures that the contains method correctly determines if a rect is
        contained within the circle"""
        c = Circle(0, 0, 10)
        r1 = Rect(0, 0, 3, 3)
        r2 = Rect(10, 10, 10, 10)
        r3 = Rect(10, 10, 5, 5)

        angle = math.pi / 4
        x = c.x - math.sin(angle) * c.r
        y = c.y - math.cos(angle) * c.r
        rx = c.x + math.sin(angle) * c.r
        ry = c.y + math.cos(angle) * c.r
        r_edge = Rect(x, y, rx - x, ry - y)

        fr1 = FRect(0, 0, 3, 3)
        fr2 = FRect(10, 10, 10, 10)
        fr3 = FRect(10, 10, 5, 5)
        fr_edge = FRect(x, y, rx - x, ry - y)

        # contained rect
        self.assertTrue(c.contains(r1))

        # not contained rect
        self.assertFalse(c.contains(r2))
        self.assertFalse(c.contains(r3))

        # on the edge
        self.assertTrue(c.contains(r_edge))

        # contained rect
        self.assertTrue(c.contains(fr1))

        # not contained rect
        self.assertFalse(c.contains(fr2))
        self.assertFalse(c.contains(fr3))

        # on the edge
        self.assertTrue(c.contains(fr_edge))


if __name__ == "__main__":
    unittest.main()
