import sys
from collections.abc import Callable, Collection, Iterator
from typing import (
    ClassVar,
    Literal,
    SupportsIndex,
    TypeVar,
    overload,
)

from pygame.typing import Point, RectLike, SequenceLike
from typing_extensions import deprecated  # added in 3.13

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from types import EllipsisType

_N = TypeVar("_N", int, float)
_K = TypeVar("_K")
_V = TypeVar("_V")
_T = TypeVar("_T")

_RectTypeCompatible_co = TypeVar(
    "_RectTypeCompatible_co", bound=RectLike, covariant=True
)

class _GenericRect(Collection[_N]):
    """Pygame object for storing rectangular coordinates.
    
    .. versionadded:: 2.2
        Added ``FRect`` class that is functionally identical to ``Rect`` but uses
        floats instead of integers, enabling fractional precision and avoiding
        truncation error while being interchangeable with standard Rects.

    Pygame uses Rect objects to store and manipulate rectangular areas. A Rect
    can be created from a combination of left, top, width, and height values.
    Rects can also be created from python objects that are already a Rect or
    have an attribute named "rect".

    Any pygame function that requires a Rect argument also accepts any of these
    values to construct a Rect. This makes it easier to create Rects on the fly
    as arguments to functions.

    If no arguments are given, a zero Rect will be created (x=0, y=0, w=0, h=0).
    This will only work when using the Rect/FRect class and not with functions
    that require a Rect argument.

    The Rect functions that change the position or size of a Rect return a new
    copy of the Rect with the affected changes. The original Rect is not
    modified. Some methods have an alternate "in-place" version that returns
    None but affects the original Rect. These "in-place" methods are denoted
    with the "ip" suffix.

    The Rect object has several virtual attributes which can be used to move and
    align the Rect:

    ::

        x,y
        top, left, bottom, right
        topleft, bottomleft, topright, bottomright
        midtop, midleft, midbottom, midright
        center, centerx, centery
        size, width, height, relcenter
        w,h

    All of these attributes can be assigned to:

    ::

        rect1.right = 10
        rect2.center = (20,30)

    Assigning to size, width, height, or relcenter changes the dimensions of the rectangle;
    all other assignments move the rectangle without resizing it. Notice that
    some attributes are integers and others are pairs of integers.

    If a Rect has a nonzero width or height, it will return ``True`` for a
    nonzero test. Some methods return a Rect with 0 size to represent an invalid
    rectangle. A Rect with a 0 size will not collide when using collision
    detection methods (e.g. :meth:`collidepoint`, :meth:`colliderect`, etc.).

    The coordinates for Rect objects are all integers. The size values can be
    programmed to have negative values, but these are considered illegal Rects
    for most operations.

    There are several collision tests between other rectangles. Most python
    containers can be searched for collisions against a single Rect.

    The area covered by a Rect does not include the right- and bottom-most edge
    of pixels. If one Rect's bottom border is another Rect's top border (i.e.,
    rect1.bottom=rect2.top), the two meet exactly on the screen but do not
    overlap, and ``rect1.colliderect(rect2)`` returns false.

    The Rect object is also iterable:

    ::

        r = Rect(0, 1, 2, 3)
        x, y, w, h = r

    .. versionaddedold:: 1.9.2
        The Rect class can be subclassed. Methods such as ``copy()`` and ``move()``
        will recognize this and return instances of the subclass.
        However, the subclass's ``__init__()`` method is not called,
        and ``__new__()`` is assumed to take no arguments. So these methods should be
        overridden if any extra attributes need to be copied.

    .. versionadded:: 2.5.6
        ``relcenter`` added to Rect / FRect. This will return a tuple containing half
        the Rect's size; the center relative to the topleft of the Rect.
        Setting it to a ``Point`` will modify the size of the rect to 2 times
        the ``Point`` given. Below you can find a code example of how it should work:

        .. code-block:: python

            >>> my_rect = pygame.Rect(0, 0, 2, 2)
            >>> my_rect.relcenter
            (1, 1)
            >>> my_rect.relcenter = (128, 128)
            >>> my_rect.size
            (256, 256)

        Beware of non-integer relative centers! For Rects (but not FRects), ``relcenter``
        will truncate the numbers in the returned tuple.
    """
    @property
    def x(self) -> _N: ...
    @x.setter
    def x(self, value: float) -> None: ...
    @property
    def y(self) -> _N: ...
    @y.setter
    def y(self, value: float) -> None: ...
    @property
    def top(self) -> _N: ...
    @top.setter
    def top(self, value: float) -> None: ...
    @property
    def left(self) -> _N: ...
    @left.setter
    def left(self, value: float) -> None: ...
    @property
    def bottom(self) -> _N: ...
    @bottom.setter
    def bottom(self, value: float) -> None: ...
    @property
    def right(self) -> _N: ...
    @right.setter
    def right(self, value: float) -> None: ...
    @property
    def topleft(self) -> tuple[_N, _N]: ...
    @topleft.setter
    def topleft(self, value: Point) -> None: ...
    @property
    def bottomleft(self) -> tuple[_N, _N]: ...
    @bottomleft.setter
    def bottomleft(self, value: Point) -> None: ...
    @property
    def topright(self) -> tuple[_N, _N]: ...
    @topright.setter
    def topright(self, value: Point) -> None: ...
    @property
    def bottomright(self) -> tuple[_N, _N]: ...
    @bottomright.setter
    def bottomright(self, value: Point) -> None: ...
    @property
    def midtop(self) -> tuple[_N, _N]: ...
    @midtop.setter
    def midtop(self, value: Point) -> None: ...
    @property
    def midleft(self) -> tuple[_N, _N]: ...
    @midleft.setter
    def midleft(self, value: Point) -> None: ...
    @property
    def midbottom(self) -> tuple[_N, _N]: ...
    @midbottom.setter
    def midbottom(self, value: Point) -> None: ...
    @property
    def midright(self) -> tuple[_N, _N]: ...
    @midright.setter
    def midright(self, value: Point) -> None: ...
    @property
    def center(self) -> tuple[_N, _N]: ...
    @center.setter
    def center(self, value: Point) -> None: ...
    @property
    def relcenter(self) -> tuple[_N, _N]: ...
    @relcenter.setter
    def relcenter(self, value: Point) -> None: ...
    @property
    def centerx(self) -> _N: ...
    @centerx.setter
    def centerx(self, value: float) -> None: ...
    @property
    def centery(self) -> _N: ...
    @centery.setter
    def centery(self, value: float) -> None: ...
    @property
    def size(self) -> tuple[_N, _N]: ...
    @size.setter
    def size(self, value: Point) -> None: ...
    @property
    def width(self) -> _N: ...
    @width.setter
    def width(self, value: float) -> None: ...
    @property
    def height(self) -> _N: ...
    @height.setter
    def height(self, value: float) -> None: ...
    @property
    def w(self) -> _N: ...
    @w.setter
    def w(self, value: float) -> None: ...
    @property
    def h(self) -> _N: ...
    @h.setter
    def h(self, value: float) -> None: ...
    __hash__: ClassVar[None]  # type: ignore[assignment]
    @overload
    def __init__(
        self, left: float, top: float, width: float, height: float, /
    ) -> None: ...
    @overload
    def __init__(self, left_top: Point, width_height: Point, /) -> None: ...
    @overload
    def __init__(self, single_arg: RectLike, /) -> None: ...
    @overload
    def __init__(self) -> None: ...
    def __len__(self) -> Literal[4]: ...
    def __iter__(self) -> Iterator[_N]: ...
    @overload
    def __getitem__(self, i: SupportsIndex) -> _N: ...
    @overload
    def __getitem__(self, s: slice | EllipsisType) -> list[_N]: ...
    @overload
    def __setitem__(self, key: int, value: float) -> None: ...
    @overload
    def __setitem__(
        self, key: slice | EllipsisType, value: float | RectLike
    ) -> None: ...
    def __copy__(self) -> Self: ...
    def copy(self) -> Self:
        """Copy the rectangle.
        
        Returns a new rectangle having the same position and size as the original.
        
        New in pygame 1.9
        """
    @overload
    def move(self, x: float, y: float, /) -> Self: ...
    @overload
    def move(self, move_by: Point, /) -> Self: 
        """Moves the rectangle.
        
        Returns a new rectangle that is moved by the given offset. The x and y
        arguments can be any integer value, positive or negative.
        """
    @overload
    def move_ip(self, x: float, y: float, /) -> None: ...
    @overload
    def move_ip(self, move_by: Point, /) -> None:
        """Moves the rectangle, in place.

        Same as the ``Rect.move()`` method, but operates in place.
        """
    def move_to(self, **kwargs: float | Point) -> Self:
        """Moves the rectangle to the specified position.

        Returns a new rectangle that is moved to the given position and optionally resized.
        You must provide keyword arguments to the method such as ``center``, ``left``,
        ``midbottom``, ``size`` that correspond to the rectangle's attributes and the
        method will return a new rectangle whose specified attributes are set to the given value.

        It is similar to :meth:`Surface.get_rect` but instead of a calling it as a surface method
        you call it as a rectangle method.

        .. versionadded:: 2.4.0
        """
    @overload
    def inflate(self, x: float, y: float, /) -> Self: ...
    @overload
    def inflate(self, inflate_by: Point, /) -> Self:
        """Grow or shrink the rectangle size.
        
        Returns a new rectangle with the size changed by the given offset. The
        rectangle remains centered around its current center. Negative values
        will shrink the rectangle. Note, uses integers, if the offset given is
        too small(< 2 > -2), center will be off.
        """
    @overload
    def inflate_ip(self, x: float, y: float, /) -> None: ...
    @overload
    def inflate_ip(self, inflate_by: Point, /) -> None:
        """Grow or shrink the rectangle size, in place.
        
        Same as the ``Rect.inflate()`` method, but operates in place.
        """
    @overload
    def scale_by(self, x: float, y: float = ...) -> Self: ...
    @overload
    def scale_by(self, scale_by: Point) -> Self:
        """Scale the rectangle by given a multiplier.
        
        Returns a new rectangle with the size scaled by the given multipliers.
        The rectangle remains centered around its current center. A single
        scalar or separate width and height scalars are allowed. Values above
        one will increase the size of the rectangle, whereas values between
        zero and one will decrease the size of the rectangle.

        .. versionadded:: 2.3.1

        .. versionchanged:: 2.5.2 the argument ``scale_by`` can now be passed as a positional argument
        """
    @overload
    def scale_by_ip(self, x: float, y: float = ...) -> None: ...
    @overload
    def scale_by_ip(self, scale_by: Point) -> None:
        """Grow or shrink the rectangle size, in place.

        Same as the ``Rect.scale_by()`` method, but operates in place.

        .. versionadded:: 2.3.1

        .. versionchanged:: 2.5.2 the argument ``scale_by`` can now be passed as a positional argument
        """
    @overload
    def update(
        self, left: float, top: float, width: float, height: float, /
    ) -> None: ...
    @overload
    def update(self, left_top: Point, width_height: Point, /) -> None: ...
    @overload
    def update(self, single_arg: RectLike, /) -> None:
        """Sets the position and size of the rectangle.

        Sets the position and size of the rectangle, in place. See
        parameters for :meth:`pygame.Rect` for the parameters of this function.

        .. versionaddedold:: 2.0.1
        """
    @overload
    def clamp(self, rect: RectLike, /) -> Self: ...
    @overload
    def clamp(self, left_top: Point, width_height: Point, /) -> Self: ...
    @overload
    def clamp(
        self, left: float, top: float, width: float, height: float, /
    ) -> Self:
        """Moves the rectangle inside another.

        Returns a new rectangle that is moved to be completely inside the
        argument Rect. If the rectangle is too large to fit inside, it is
        centered inside the argument Rect, but its size is not changed.
        """
    @overload
    def clamp_ip(self, rect: RectLike, /) -> None: ...
    @overload
    def clamp_ip(self, left_top: Point, width_height: Point, /) -> None: ...
    @overload
    def clamp_ip(
        self, left: float, top: float, width: float, height: float, /
    ) -> None:
        """Moves the rectangle inside another, in place.
        
        Same as the ``Rect.clamp()`` method, but operates in place.
        """
    @overload
    def clip(self, rect: RectLike, /) -> Self: ...
    @overload
    def clip(self, left_top: Point, width_height: Point, /) -> Self: ...
    @overload
    def clip(self, left: float, top: float, width: float, height: float, /) -> Self:
        """Crops a rectangle inside another.
        
        Returns a new rectangle that is cropped to be completely inside the
        argument Rect. If the two rectangles do not overlap to begin with, a Rect
        with 0 size is returned.
        """
    @overload
    def clipline(
        self, x1: float, x2: float, x3: float, x4: float, /
    ) -> tuple[tuple[_N, _N], tuple[_N, _N]] | tuple[()]: ...
    @overload
    def clipline(
        self, first_point: Point, second_point: Point, /
    ) -> tuple[tuple[_N, _N], tuple[_N, _N]] | tuple[()]: ...
    @overload
    def clipline(
        self, rect_arg: RectLike, /
    ) -> tuple[tuple[_N, _N], tuple[_N, _N]] | tuple[()]:
        """Crops a line inside a rectangle.

        Returns the coordinates of a line that is cropped to be completely inside
        the rectangle. If the line does not overlap the rectangle, then an empty
        tuple is returned.

        The line to crop can be any of the following formats (floats can be used
        in place of ints, but they will be truncated):

            - four ints
            - 2 lists/tuples/Vector2s of 2 ints
            - a list/tuple of four ints
            - a list/tuple of 2 lists/tuples/Vector2s of 2 ints

        :returns: a tuple with the coordinates of the given line cropped to be
            completely inside the rectangle is returned, if the given line does
            not overlap the rectangle, an empty tuple is returned
        :rtype: tuple(tuple(int, int), tuple(int, int)) or ()

        :raises TypeError: if the line coordinates are not given as one of the
            above described line formats

        .. note ::
            This method can be used for collision detection between a rect and a
            line. See example code below.

        .. note ::
            The ``rect.bottom`` and ``rect.right`` attributes of a
            :mod:`pygame.Rect` always lie one pixel outside of its actual border.

        ::

            # Example using clipline().
            clipped_line = rect.clipline(line)

            if clipped_line:
                # If clipped_line is not an empty tuple then the line
                # collides/overlaps with the rect. The returned value contains
                # the endpoints of the clipped line.
                start, end = clipped_line
                x1, y1 = start
                x2, y2 = end
            else:
                print("No clipping. The line is fully outside the rect.")

        .. versionaddedold:: 2.0.0
        """
    @overload
    def union(self, rect: RectLike, /) -> Self: ...
    @overload
    def union(self, left_top: Point, width_height: Point, /) -> Self: ...
    @overload
    def union(
        self, left: float, top: float, width: float, height: float, /
    ) -> Self:
        """Joins two rectangles into one.

        Returns a new rectangle that completely covers the area of the two
        provided rectangles. There may be area inside the new Rect that is not
        covered by the originals.
        """
    @overload
    def union_ip(self, rect: RectLike, /) -> None: ...
    @overload
    def union_ip(self, left_top: Point, width_height: Point, /) -> None: ...
    @overload
    def union_ip(
        self, left: float, top: float, width: float, height: float, /
    ) -> None:
        """Joins two rectangles into one, in place.

        Same as the ``Rect.union()`` method, but operates in place.
        """
    def unionall(self, rect: SequenceLike[_RectTypeCompatible_co], /) -> Self:
        """The union of many rectangles.
        
        Returns the union of one rectangle with a sequence of many rectangles.
        """
    def unionall_ip(
        self, rect_SequenceLike: SequenceLike[_RectTypeCompatible_co], /
    ) -> None:
        """The union of many rectangles, in place.

        The same as the ``Rect.unionall()`` method, but operates in place.
        """
    @overload
    def fit(self, rect: RectLike, /) -> Self: ...
    @overload
    def fit(self, left_top: Point, width_height: Point, /) -> Self: ...
    @overload
    def fit(self, left: float, top: float, width: float, height: float, /) -> Self:
        """Resize and move a rectangle with aspect ratio.

        Returns a new rectangle that is moved and resized to fit another. The
        aspect ratio of the original Rect is preserved, so the new rectangle may
        be smaller than the target in either width or height.
        """
    def normalize(self) -> None:
        """Correct negative sizes.
        
        This will flip the width or height of a rectangle if it has a negative
        size. The rectangle will remain in the same place, with only the sides
        swapped.
        """
    def __contains__(self, rect: RectLike | _N, /) -> bool: # type: ignore[override]
        """Test if one rectangle is inside another.
        
        Returns true when the argument is completely inside the Rect."""
    @overload
    def contains(self, rect: RectLike, /) -> bool: ...
    @overload
    def contains(self, left_top: Point, width_height: Point, /) -> bool: ...
    @overload
    def contains(
        self, left: float, top: float, width: float, height: float, /
    ) -> bool:
        """Test if one rectangle is inside another.
        
        Returns true when the argument is completely inside the Rect."""
    @overload
    def collidepoint(self, x: float, y: float, /) -> bool: ...
    @overload
    def collidepoint(self, x_y: Point, /) -> bool:
        """Test if a point is inside a rectangle.

        Returns true if the given point is inside the rectangle. A point along
        the right or bottom edge is not considered to be inside the rectangle.

        .. note ::
            For collision detection between a rect and a line the :meth:`clipline`
            method can be used.
        """
    @overload
    def colliderect(self, rect: RectLike, /) -> bool: ...
    @overload
    def colliderect(self, left_top: Point, width_height: Point, /) -> bool: ...
    @overload
    def colliderect(
        self, left: float, top: float, width: float, height: float, /
    ) -> bool:
        """Test if two rectangles overlap.

        Returns true if any portion of either rectangle overlap (except the
        top+bottom or left+right edges).

        .. note ::
            For collision detection between a rect and a line the :meth:`clipline`
            method can be used.
        """
    def collidelist(
        self, rect_list: SequenceLike[_RectTypeCompatible_co], /
    ) -> int:
        """Test if one rectangle in a list intersects.
        
        Test whether the rectangle collides with any in a sequence of rectangles.
        The index of the first collision found is returned. If no collisions are
        found an index of -1 is returned.
        """
    def collidelistall(
        self, rect_list: SequenceLike[_RectTypeCompatible_co], /
    ) -> list[int]:
        """Test if all rectangles in a list intersect.
        
        Returns a list of all the indices that contain rectangles that collide
        with the Rect. If no intersecting rectangles are found, an empty list is
        returned.

        Not only Rects are valid arguments, but these are all valid calls:

        .. code-block:: python
            :linenos:

            Rect = pygame.Rect
            r = Rect(0, 0, 10, 10)

            list_of_rects = [Rect(1, 1, 1, 1), Rect(2, 2, 2, 2)]
            indices0 = r.collidelistall(list_of_rects)

            list_of_lists = [[1, 1, 1, 1], [2, 2, 2, 2]]
            indices1 = r.collidelistall(list_of_lists)

            list_of_tuples = [(1, 1, 1, 1), (2, 2, 2, 2)]
            indices2 = r.collidelistall(list_of_tuples)

            list_of_double_tuples = [((1, 1), (1, 1)), ((2, 2), (2, 2))]
            indices3 = r.collidelistall(list_of_double_tuples)

            class ObjectWithRectAttribute(object):
                def __init__(self, r):
                    self.rect = r

            list_of_object_with_rect_attribute = [
                ObjectWithRectAttribute(Rect(1, 1, 1, 1)),
                ObjectWithRectAttribute(Rect(2, 2, 2, 2)),
            ]
            indices4 = r.collidelistall(list_of_object_with_rect_attribute)

            class ObjectWithCallableRectAttribute(object):
                def __init__(self, r):
                    self._rect = r

                def rect(self):
                    return self._rect

            list_of_object_with_callable_rect = [
                ObjectWithCallableRectAttribute(Rect(1, 1, 1, 1)),
                ObjectWithCallableRectAttribute(Rect(2, 2, 2, 2)),
            ]
            indices5 = r.collidelistall(list_of_object_with_callable_rect)
        """
    def collideobjects(
        self, objects: SequenceLike[_T], key: Callable[[_T], RectLike] | None = None
    ) -> _T | None:
        """Test if any object in a list intersects.
        
        Test whether the rectangle collides with any object in the sequence.
        The object of the first collision found is returned. If no collisions are
        found then ``None`` is returned

        If key is given, then it should be a method taking an object from the list
        as input and returning a rect like object e.g. ``lambda obj: obj.rectangle``.
        If an object has multiple attributes of type Rect then key could return one
        of them.

        .. code-block:: python
            :linenos:

            r = Rect(1, 1, 10, 10)

            rects = [
                Rect(1, 1, 10, 10),
                Rect(5, 5, 10, 10),
                Rect(15, 15, 1, 1),
                Rect(2, 2, 1, 1),
            ]

            result = r.collideobjects(rects)  # -> <rect(1, 1, 10, 10)>
            print(result)

            class ObjectWithSomRectAttribute:
                def __init__(self, name, collision_box, draw_rect):
                    self.name = name
                    self.draw_rect = draw_rect
                    self.collision_box = collision_box

                def __repr__(self):
                    return f'<{self.__class__.__name__}("{self.name}", {list(self.collision_box)}, {list(self.draw_rect)})>'

            objects = [
                ObjectWithSomRectAttribute("A", Rect(15, 15, 1, 1), Rect(150, 150, 50, 50)),
                ObjectWithSomRectAttribute("B", Rect(1, 1, 10, 10), Rect(300, 300, 50, 50)),
                ObjectWithSomRectAttribute("C", Rect(5, 5, 10, 10), Rect(200, 500, 50, 50)),
            ]

            # collision = r.collideobjects(objects) # this does not work because the items in the list are no Rect like object
            collision = r.collideobjects(
                objects, key=lambda o: o.collision_box
            )  # -> <ObjectWithSomRectAttribute("B", [1, 1, 10, 10], [300, 300, 50, 50])>
            print(collision)

            screen_rect = r.collideobjects(objects, key=lambda o: o.draw_rect)  # -> None
            print(screen_rect)

        .. versionadded:: 2.1.3
        """
    def collideobjectsall(
        self, objects: SequenceLike[_T], key: Callable[[_T], RectLike] | None = None
    ) -> list[_T]:
        """Test if all objects in a list intersect.
        
        Returns a list of all the objects that contain rectangles that collide
        with the Rect. If no intersecting objects are found, an empty list is
        returned.

        If key is given, then it should be a method taking an object from the list
        as input and returning a rect like object e.g. ``lambda obj: obj.rectangle``.
        If an object has multiple attributes of type Rect then key could return one
        of them.

        .. code-block:: python
            :linenos:

            r = Rect(1, 1, 10, 10)

            rects = [
                Rect(1, 1, 10, 10),
                Rect(5, 5, 10, 10),
                Rect(15, 15, 1, 1),
                Rect(2, 2, 1, 1),
            ]

            result = r.collideobjectsall(
                rects
            )  # -> [<rect(1, 1, 10, 10)>, <rect(5, 5, 10, 10)>, <rect(2, 2, 1, 1)>]
            print(result)

            class ObjectWithSomRectAttribute:
                def __init__(self, name, collision_box, draw_rect):
                    self.name = name
                    self.draw_rect = draw_rect
                    self.collision_box = collision_box

                def __repr__(self):
                    return f'<{self.__class__.__name__}("{self.name}", {list(self.collision_box)}, {list(self.draw_rect)})>'

            objects = [
                ObjectWithSomRectAttribute("A", Rect(1, 1, 10, 10), Rect(300, 300, 50, 50)),
                ObjectWithSomRectAttribute("B", Rect(5, 5, 10, 10), Rect(200, 500, 50, 50)),
                ObjectWithSomRectAttribute("C", Rect(15, 15, 1, 1), Rect(150, 150, 50, 50)),
            ]

            # collisions = r.collideobjectsall(objects) # this does not work because ObjectWithSomRectAttribute is not a Rect like object
            collisions = r.collideobjectsall(
                objects, key=lambda o: o.collision_box
            )  # -> [<ObjectWithSomRectAttribute("A", [1, 1, 10, 10], [300, 300, 50, 50])>, <ObjectWithSomRectAttribute("B", [5, 5, 10, 10], [200, 500, 50, 50])>]
            print(collisions)

            screen_rects = r.collideobjectsall(objects, key=lambda o: o.draw_rect)  # -> []
            print(screen_rects)

        .. versionadded:: 2.1.3
        """
    @overload
    def collidedict(
        self,
        rect_dict: dict[_RectTypeCompatible_co, _V],
        values: Literal[False] = False,
    ) -> tuple[_RectTypeCompatible_co, _V] | None: ...
    @overload
    def collidedict(
        self, rect_dict: dict[_K, _RectTypeCompatible_co], values: Literal[True]
    ) -> tuple[_K, _RectTypeCompatible_co] | None:
        """Test if one rectangle in a dictionary intersects.

        Returns the first key and value pair that intersects with the calling
        Rect object. If no collisions are found, ``None`` is returned. If
        ``values`` is False (default) then the dict's keys will be used in the
        collision detection, otherwise the dict's values will be used.

        .. note ::
            Rect objects cannot be used as keys in a dictionary (they are not
            hashable), so they must be converted to a tuple.
            e.g. ``rect.collidedict({tuple(key_rect) : value})``

        .. versionchanged:: 2.4.0
            ``values`` is now accepted as a keyword argument. Type Stub updated
            to use boolean ``True`` or ``False``, but any truthy or falsy value
            will be valid.
        """
    @overload
    def collidedictall(
        self,
        rect_dict: dict[_RectTypeCompatible_co, _V],
        values: Literal[False] = False,
    ) -> list[tuple[_RectTypeCompatible_co, _V]]: ...
    @overload
    def collidedictall(
        self, rect_dict: dict[_K, _RectTypeCompatible_co], values: Literal[True]
    ) -> list[tuple[_K, _RectTypeCompatible_co]]:
        """Test if all rectangles in a dictionary intersect.

        Returns a list of all the key and value pairs that intersect with the
        calling Rect object. If no collisions are found an empty list is returned.
        If ``values`` is False (default) then the dict's keys will be used in the
        collision detection, otherwise the dict's values will be used.

        .. note ::
            Rect objects cannot be used as keys in a dictionary (they are not
            hashable), so they must be converted to a tuple.
            e.g. ``rect.collidedictall({tuple(key_rect) : value})``

        .. versionchanged:: 2.4.0
            ``values`` is now accepted as a keyword argument. Type Stub updated
            to use boolean ``True`` or ``False``, but any truthy or falsy value
            will be valid.
        """

# Rect confirms to the Collection ABC, since it also confirms to
# Sized, Iterable and Container ABCs
class Rect(_GenericRect[int]): ...
class FRect(_GenericRect[float]): ...

@deprecated("Use `Rect` instead (RectType is an old alias)")
class RectType(Rect): ...

@deprecated("Use `FRect` instead (FRectType is an old alias)")
class FRectType(FRect): ...
