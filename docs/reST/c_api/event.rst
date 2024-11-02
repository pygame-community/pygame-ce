.. include:: ../common.txt

.. highlight:: c

********************************
  API exported by pygame.event
********************************

src_c/event.c
=============

The extension module :py:mod:`pygame.event`.

Header file: src_c/include/pygame.h

.. c:function:: PyObject* pgEvent_GetType(void)

   Return a python class that is currently set to be the event class

   If the class is not known at the time (called before ``pygame._event.register_event_class``)
   this function will return NULL and set the error.

.. c:function:: int pgEvent_Check(PyObject *x)

   Return true if *x* is a pygame event instance

   Will return false if *x* is a subclass of event.
   Will return -1 if python error is set while checking.
   No check is made that *x* is not ``NULL``.

.. c:function:: PyObject* pgEvent_New(SDL_Event *event)

   Return a new pygame event instance for the SDL *event*.
   If *event* is ``NULL`` then create an empty event object.
   On failure raise a Python exception and return ``NULL``.

   .. note::
      This is a destructive operation, so don't use passed SDL_Event afterwards.

.. c:function:: PyObject* pgEvent_FromTypeAndDict(int e_type, PyObject *dict)

   Instantiates a new Event object created from the given event type and a dict.

   On error returns NULL and sets python exception.

.. c:function:: int pgEvent_GetEventType(PyObject *)

   Returns an event type extracted from the python object.

   On error this retuns -1.

.. c:function:: char* pgEvent_GetKeyDownInfo(void)

   Return an array of bools (using char) of length SDL_NUM_SCANCODES
   with the most recent key presses.

.. c:function:: char* pgEvent_GetKeyUpInfo(void)

   Return an array of bools (using char) of length SDL_NUM_SCANCODES
   with the most recent key releases.

.. c:function:: char* pgEvent_GetMouseButtonDownInfo(void)

   Return an array of bools (using char) of length 5
   with the most recent button presses.

.. c:function:: char* pgEvent_GetMouseButtonUpInfo(void)

   Return an array of bools (using char) of length 5
   with the most recent button releases.

.. c:function:: int pg_post_event(Uint32 type, PyObject *obj)

   Posts a pygame event that is an ``SDL_USEREVENT`` on the SDL side. This
   function takes a python dict or Event instance, which can be NULL too.
   This function does not need GIL to be held if obj is NULL, but needs GIL
   otherwise. Just like the SDL ``SDL_PushEvent`` function, returns 1 on
   success, 0 if the event was not posted due to it being blocked, and -1 on
   failure.

   .. ## pg_post_event ##

.. c:function:: int pg_post_event_steal(Uint32 type, PyObject *obj)

   Nearly the same as :c:func:`pg_post_event`, but with two differences.
   1) This doesn't need GIL held at all when called.
   2) This steals the reference to obj, instead of borrowing it.
