.. include:: ../common.txt

.. highlight:: c

********************************************
  Class Color API exported by pygame.color
********************************************

src_c/color.c
=============

This extension module defines the Python type :py:class:`pygame.Color`.

Header file: src_c/include/pygame.h


.. c:var:: PyTypeObject *pgColor_Type

   The Pygame color object type :py:class:`pygame.Color`.

.. c:function:: int pgColor_CheckExact(PyObject *obj)

   Return true if *obj* is an instance of type pgColor_Type,
   but not a pgColor_Type subclass instance.
   This macro does not check if *obj* is not ``NULL`` or indeed a Python type.

.. c:function:: PyObject* pgColor_New(Uint8 rgba[])

   Return a new :py:class:`pygame.Color` instance from the four element array *rgba*.
   On failure, raise a Python exception and return ``NULL``.

.. c:function:: PyObject* pgColor_NewLength(Uint8 rgba[], Uint8 length)

   Return a :py:class:`new pygame.Color` instance having *length* elements,
   with element values taken from the first *length* elements of array *rgba*.
   Argument *length* must be between ``1`` and ``4`` inclusive.
   On failure, raise a Python exception and return ``NULL``.

.. c:function:: int pg_RGBAFromObjEx(PyObject *color, Uint8 rgba[], pgColorHandleFlags handle_flags)

   Set the four element array *rgba* to the color represented by object *color*.
   Return ``1`` on success, ``0`` otherwise and sets a python exception.
   This in an extension of :c:func:`pg_RGBAFromObj` optimized for pgColor_Type
   instances and tuples. It can also handle integer and string color inputs based
   on ``handle_flags``.

.. c:function:: int pg_MappedColorFromObj(PyObject *val, SDL_Surface *surf, Uint32 *color, pgColorHandleFlags handle_flags)

   Like above function, but returns mapped color instead. One notable point of difference is
   the way in which ints are handled (this function directly interprets the int passed as the
   mapped color on the surface ``surf```)
