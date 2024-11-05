.. include:: ../common.txt

.. highlight:: c

********************************
  API exported by pygame.event
********************************

src_c/event.c
=============

The extension module :py:mod:`pygame.event`.

Header file: src_c/include/pygame.h

.. c:type:: pgEventData

   Struct holding information about the event object.

   .. c:member:: int type

      The event type code.

   .. c:member:: PyObject* dict

      Dict object of the event, might be NULL.

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

.. c:function:: PyObject* pgEvent_FromEventData(pgEventData)

   Return an event object constructed from pgEventData struct.

   On error returns NULL and sets python exception.

.. c:function:: pgEventData pgEvent_GetEventData(PyObject *)

   Return a pgEventData struct containing information about event extracted from the python object.

   Beware: on error this doesn't retun any special sentiel value if error ocurred, only sets python exception, so use ``PyErr_Ocurred()`` for error checking.
   Remember to call :c:func:`pgEvent_FreeEventData` after usage to avoid memory leaks.

.. c:function:: void pgEvent_FreeEventData(pgEventData)

   Free resources held by pgEventData (decrefs dict).

   .. ## pgEvent_FreeEventData ##

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

.. c:function:: int pg_post_event(Uint32 type, PyObject *dict)

   Posts a pygame event that is an ``SDL_USEREVENT`` on the SDL side. This
   function takes a python dict, which can be NULL too.
   This function does not need GIL to be held if dict is NULL, but needs GIL
   otherwise. Just like the SDL ``SDL_PushEvent`` function, returns 1 on
   success, 0 if the event was not posted due to it being blocked, and -1 on
   failure.

.. c:function:: int pg_post_event_dictproxy(Uint32 type, pgEventDictProxy *dict_proxy)

   Posts a pygame event that is an ``SDL_USEREVENT`` on the SDL side, can also
   optionally take a dictproxy instance. Using this dictproxy API is especially
   useful when multiple events that need to be posted share the same dict
   attribute, like in the case of event timers. This way, the number of python
   increfs and decrefs are reduced, and callers of this function don't need to
   hold GIL for every event posted, the GIL only needs to be held during the
   creation of the dictproxy instance, and when it is freed.
   Just like the SDL ``SDL_PushEvent`` function, returns 1 on success, 0 if the
   event was not posted due to it being blocked, and -1 on failure.
