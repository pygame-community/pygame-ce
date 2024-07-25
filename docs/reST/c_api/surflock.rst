.. include:: ../common.txt

.. highlight:: c

***********************************
  API exported by pygame.surflock
***********************************

src_c/surflock.c
================

This extension module implements SDL surface locking for the
:py:class:`pygame.Surface` type.

Header file: src_c/include/pygame.h


.. c:function:: void pgSurface_Prep(pgSurfaceObject *surfobj)

   If *surfobj* is a subsurface, then lock the parent surface with *surfobj*
   the owner of the lock.

.. c:function:: void pgSurface_Unprep(pgSurfaceObject *surfobj)

   If *surfobj* is a subsurface, then release its lock on the parent surface.

.. c:function:: int pgSurface_Lock(pgSurfaceObject *surfobj)

   Lock pygame surface *surfobj*, with *surfobj* owning its own lock.

.. c:function:: int pgSurface_LockBy(pgSurfaceObject *surfobj, PyObject *lockobj)

   Lock pygame surface *surfobj* with Python object *lockobj* the owning
   the lock.

   The surface will keep a weak reference to object *lockobj*,
   and eventually remove the lock on itself if *lockobj* is garbage collected.
   However, it is best if *lockobj* also keep a reference to the locked surface
   and call to :c:func:`pgSurface_UnLockBy` when finished with the surface.

.. c:function:: int pgSurface_UnLock(pgSurfaceObject *surfobj)

   Remove the pygame surface *surfobj* object's lock on itself.

.. c:function:: int pgSurface_UnLockBy(pgSurfaceObject *surfobj, PyObject *lockobj)

   Remove the lock on pygame surface *surfobj* owned by Python object *lockobj*.
