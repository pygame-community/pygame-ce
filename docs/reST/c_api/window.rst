.. include:: ../common.txt

.. highlight:: c

************************************************
  Class Window API exported by pygame.window
************************************************

src_c/window.c
===============

This extension module defines Python type :py:class:`pygame.Window`.

Header file: src_c/include/pygame.h


.. c:type:: pgWindowObject

   A :py:class:`pygame.window.Window` instance.

.. c:var:: PyTypeObject *pgWindow_Type

   The :py:class:`pygame.window.Window` Python type.

.. c:function:: int pgWindow_Check(PyObject *x)

   Return true if *x* is a :py:class:`pygame.window.Window` instance

   Will return false if *x* is not a subclass of `Window`.
   This is a macro. No check is made that *x* is not *NULL*.
