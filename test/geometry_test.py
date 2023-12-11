import unittest
import math

from math import sqrt
from pygame import Vector2, Vector3, Rect, FRect

from pygame.geometry import Circle


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

        for value in (-10.3234, -1, 0, 0.0):
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

        for value in (-10.3234, -1, 0, 0.0):
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

        for value in (-10.3234, -1, 0, 0.0):
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

        for value in (-10.3234, -1, 0, 0.0):
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


if __name__ == "__main__":
    unittest.main()
