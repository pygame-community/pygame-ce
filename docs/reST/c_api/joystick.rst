.. include:: ../common.txt

.. highlight:: c

******************************************
    API exported by pygame.joystick
******************************************

src_c/joystick.c
================

The extension module :py:mod:`pygame.joystick`.

Header file: src_c/include/pygame.h

.. c:var:: PyTypeObject *pgJoystick_Type

   The Pygame joystick object type :py:class:`pygame.Joystick`.

.. c:function:: PyObject* pgJoystick_New(int id)

   Return a new :py:class:`pygame.Joystick` instance.
   On failure, raise a Python exception and return ``NULL``.

.. c:function:: int pgJoystick_GetDeviceIndexByInstanceID(int instance_id)

   Get the device index of a joystick by a instance id.
   Return a device index.
   On failure, it returns -1.
