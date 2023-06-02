.. include:: ../common.txt

.. highlight:: c

******************************************
  High level API exported by pygame.image
******************************************

src_c/image.c
=============

The extension module :py:mod:`pygame.image`.

C header: src_c/include/pygame.h

.. c:function:: PyObject* pgImage_LoadBasic(PyObject *fileobj)

    Equivalent to :func:`pygame.image.load_basic`.
    Returns *NULL* on failure.
