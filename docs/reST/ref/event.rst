.. include:: common.txt

:mod:`pygame.event`
===================

.. module:: pygame.event
   :synopsis: pygame module for interacting with events and queues

| :sl:`pygame module for interacting with events and queues`

.. rubric:: Event queue

Pygame handles all its event messaging through an event queue. The functions in
this module help you manage that event queue. The input queue is heavily
dependent on the video system (:mod:`pygame.display` or :class:`pygame.Window`).
If a window has not been created, the event queue may not work properly.

The event queue has an upper limit on the number of events it can hold. When
the queue becomes full new events are quietly dropped. To prevent lost events,
especially input events which signal a quit command, your program must handle
events every frame (with :func:`pygame.event.get()`, :func:`pygame.event.pump()`,
:func:`pygame.event.wait()`, :func:`pygame.event.peek()` or
:func:`pygame.event.clear()`).

.. note:: Not handling events may cause the system to decide the program is
   frozen (not responding).

.. rubric:: Events of input devices

To get the state of various input devices, you can forego the event queue and
access the input devices directly with their appropriate modules:
:mod:`pygame.mouse`, :mod:`pygame.key`, and :mod:`pygame.joystick`. However,
the event queue still needs to be running internally to enable this; programs
still need to use functions like :func:`pygame.event.get()` or
:func:`pygame.event.pump()` periodically. Note: Joysticks will not send any
events until the device has been initialized.

.. rubric:: Event objects

The event queue contains :class:`pygame.event.Event` event objects.
There are a variety of ways to access the queued events, from simply
checking for the existence of events, to popping them off of the event queue.

All :class:`pygame.event.Event` instances contain an event type identifier
and attributes specific to that event type. The event type identifier is
accessible as the :attr:`pygame.event.Event.type` property. An event type's
specific attributes can be accessed directly as an attribute on the event
object.

Users can create their own new events (or emulate system events) by
instantiating :func:`pygame.event.Event()` themselves, usually paired
with :func:`pygame.event.post()`.

Events support equality and inequality comparisons. Two events are equal if
they are the same type and have identical attribute values.

.. rubric:: Custom events and debugging

The event type identifier is in between the values of ``NOEVENT`` and
``NUMEVENTS``. User defined events should have a value in the inclusive range
of ``USEREVENT`` to ``NUMEVENTS - 1``. User defined events should reserve
a custom event number with :func:`pygame.event.custom_type()`.

While debugging and experimenting, you can print an event object for a quick
display of its type and members.

.. rubric:: Event types and attributes

Events that come from the system will have a guaranteed set of member
attributes based on the type. The following are lists of event types with their
specific attributes and notes.

You can also find a list of constants for keyboard keys
:ref:`here <key-constants-label>`.

::

    Event type                 Attributes/Notes

    QUIT
    USEREVENT                  (Starting type of the user defined
                                event types)

    KEYDOWN                    key, mod, unicode, scancode, window(1)
    KEYUP                      key, mod, unicode, scancode, window(1)

    MOUSEMOTION                pos, rel, buttons, touch(2), window(1)
    MOUSEBUTTONUP              pos, button, touch(2), clicks(3), window(1)
    MOUSEBUTTONDOWN            pos, button, touch(2), clicks(3), window(1)
    MOUSEWHEEL                 which, flipped, x, y, touch(2), precise_x,
                                precise_y, window(1)

    JOYAXISMOTION              instance_id, axis, value (deprecated: joy)
    JOYBALLMOTION              instance_id, ball, rel (deprecated: joy)
    JOYHATMOTION               instance_id, hat, value (deprecated: joy)
    JOYBUTTONUP                instance_id, button (deprecated: joy)
    JOYBUTTONDOWN              instance_id, button (deprecated: joy)
    CONTROLLERDEVICEADDED      device_index
    JOYDEVICEADDED             device_index
    CONTROLLERDEVICEREMOVED    instance_id
    JOYDEVICEREMOVED           instance_id
    CONTROLLERDEVICEREMAPPED   instance_id

    (Use the window event API instead of legacy events)
    ACTIVEEVENT                gain, state (Legacy event)
    VIDEORESIZE                size, w, h  (Legacy event)
    VIDEOEXPOSE                            (Legacy event)

    AUDIODEVICEADDED           which, iscapture
    AUDIODEVICEREMOVED         which, iscapture

    FINGERMOTION               touch_id, finger_id, x, y, dx, dy, window(1)
    FINGERDOWN                 touch_id, finger_id, x, y, dx, dy, window(1)
    FINGERUP                   touch_id, finger_id, x, y, dx, dy, window(1)
    MULTIGESTURE               touch_id, x, y, pinched, rotated, num_fingers

    TEXTEDITING(4)             text, start(4), length(4), window(1)
    TEXTINPUT(4)               text, window(1)

    DROPFILE                   window(1), file (Path of the file dropped
                                on the window)
    DROPBEGIN                  window(1)
    DROPCOMPLETE               window(1)
    DROPTEXT                   window(1)

    MIDIIN                     (Reserved for pygame.midi use)
    MIDIOUT                    (Reserved for pygame.midi use)

    KEYMAPCHANGED              (Keymap change due to language/keyboard
                                layout change)
    CLIPBOARDUPDATE            (Partially experimental)
    LOCALECHANGED

    RENDER_TARGETS_RESET
    RENDER_DEVICE_RESET

|

(``1``): if a :class:`pygame.Window` instance exists for the window that the event
occurred in, the ``window`` attribute of these events will be that instance,
otherwise it will be ``None``.

(``2``): The ``touch`` attribute of ``MOUSE`` events indicates whether or not the
events were generated by a touch input device, and not a real mouse. You might
want to ignore such events, if your application already handles ``FINGERMOTION``,
``FINGERDOWN`` and ``FINGERUP`` events.

(``3``): The ``clicks`` attribute of the ``MOUSEBUTTONDOWN`` and ``MOUSEBUTTONUP``
events indicate the number of clicks occurring in rapid succession, e.g. ``1``
for single-click, ``2`` for double-click, etc. Note that double, triple, or
more clicks will still fire mouse events for each individual click, with a
progressively increasing ``clicks`` attribute.

(``4``): The ``start`` attribute of the ``TEXTEDITING`` event is the cursor position,
in UTF-8 characters, where the new typing will be inserted into the editing text,
while the ``length`` attribute is the number of UTF-8 characters that will be
replaced by the new typing.

These ``TEXT*`` events are useful to implement inputs/languages that require composition,
provided by the system's IME (Input Method Editor). The ``TEXTINPUT`` event is only
fired when the text is confirmed.

|

Here is a list of the new window events.

All window events have a ``window`` attribute corresponding to the
:class:`pygame.Window` that generated them.

::

   Event type             Short description and additional attributes

   WINDOWSHOWN            Window became shown
   WINDOWHIDDEN           Window became hidden
   WINDOWEXPOSED          Window got updated by some external event
   WINDOWMOVED            Window got moved        (x, y attributes)
   WINDOWSIZECHANGED      Window size has changed (x, y attributes)
   WINDOWRESIZED          Window got resized by the user/window manager
                           (x, y attributes)
   WINDOWMINIMIZED        Window was minimized
   WINDOWMAXIMIZED        Window was maximized
   WINDOWRESTORED         Window was restored
   WINDOWENTER            Mouse entered the window
   WINDOWLEAVE            Mouse left the window
   WINDOWFOCUSGAINED      Window gained focus
   WINDOWFOCUSLOST        Window lost focus
   WINDOWCLOSE            Window was closed
   WINDOWTAKEFOCUS        Window was offered focus
   WINDOWHITTEST          Window has a special hit test
   WINDOWICCPROFCHANGED   Window ICC profile changed
                           (SDL backend >= 2.0.18)
   WINDOWDISPLAYCHANGED   Window moved on a new display (display_index
                           attribute. SDL backend >= 2.0.18)

|

On Android, the following events can be generated:

::

   Event type                Short description

   APP_TERMINATING           OS is terminating the application
   APP_LOWMEMORY             OS is low on memory (try to free memory)
   APP_WILLENTERBACKGROUND   Application is entering background
   APP_DIDENTERBACKGROUND    Application entered background
   APP_WILLENTERFOREGROUND   Application is entering foreground
   APP_DIDENTERFOREGROUND    Application entered foreground

|

.. versionchangedold:: 2.0.0 The ``joy`` attribute was deprecated, ``instance_id`` was added.

.. versionaddedold:: 2.0.1 Window events and the ``unicode`` attribute for ``KEYUP`` events.

.. versionaddedold:: 2.0.2 The ``touch`` attribute was added to all the ``MOUSE`` events.

.. versionadded:: 2.1.3 Android events, ``precise_x`` and ``precise_y`` to ``MOUSEWHEEL`` events,
   ``KEYMAPCHANGED``, ``CLIPBOARDUPDATE``, ``LOCALECHANGED``, ``WINDOWICCPROFCHANGED``,
   ``WINDOWDISPLAYCHANGED``, ``RENDER_TARGETS_RESET``, and ``RENDER_DEVICE_RESET``.

.. versionadded:: 2.5.7 The ``clicks`` attribute was added to ``MOUSEBUTTONDOWN``
   and ``MOUSEBUTTONUP`` events.

|

.. function:: pump

   | :sl:`internally process pygame event handlers`
   | :sg:`pump() -> None`

   For each frame of your game, you will need to make some sort of call to the
   event queue. This ensures your program can internally interact with the rest
   of the operating system. If you are not using other event functions in your
   game, you should call ``pygame.event.pump()`` to allow pygame to handle
   internal actions.

   This function is not necessary if your program is consistently processing
   events on the queue through the other :mod:`pygame.event` functions.

   There are important things that must be dealt with internally in the event
   queue. The main window may need to be repainted or respond to the system. If
   you fail to make a call to the event queue for too long, the system may
   decide your program has locked up.

   .. caution::
      This function should only be called in the thread that initialized :mod:`pygame.display`.

   .. ## pygame.event.pump ##

.. function:: get

   | :sl:`get events from the queue`
   | :sg:`get(eventtype=None) -> Eventlist`
   | :sg:`get(eventtype=None, pump=True) -> Eventlist`
   | :sg:`get(eventtype=None, pump=True, exclude=None) -> Eventlist`

   This will get all the messages and remove them from the queue. If a type or
   sequence of types is given only those messages will be removed from the
   queue and returned.

   If a type or sequence of types is passed in the ``exclude`` argument
   instead, then all only *other* messages will be removed from the queue. If
   an ``exclude`` parameter is passed, the ``eventtype`` parameter *must* be
   None.

   If you are only taking specific events from the queue, be aware that the
   queue could eventually fill up with the events you are not interested.

   If ``pump`` is ``True`` (the default), then :func:`pygame.event.pump()` will be called.

   .. versionchangedold:: 1.9.5 Added ``pump`` argument
   .. versionchangedold:: 2.0.2 Added ``exclude`` argument

   .. ## pygame.event.get ##

.. function:: poll

   | :sl:`get a single event from the queue`
   | :sg:`poll() -> Event instance`

   Returns a single event from the queue. If the event queue is empty an event
   of type ``pygame.NOEVENT`` will be returned immediately. The returned event
   is removed from the queue.

   .. caution::
      This function should only be called in the thread that initialized :mod:`pygame.display`.

   .. ## pygame.event.poll ##

.. function:: wait

   | :sl:`wait for a single event from the queue`
   | :sg:`wait() -> Event instance`
   | :sg:`wait(timeout) -> Event instance`

   Returns a single event from the queue. If the queue is empty this function
   will wait until one is created. From pygame 2.0.0, if a ``timeout`` argument
   is given, the function will return an event of type ``pygame.NOEVENT``
   if no events enter the queue in ``timeout`` milliseconds. The event is removed
   from the queue once it has been returned. While the program is waiting it will
   sleep in an idle state. This is important for programs that want to share the
   system with other applications.

   .. versionchangedold:: 2.0.0.dev13 Added ``timeout`` argument

   .. caution::
      This function should only be called in the thread that initialized :mod:`pygame.display`.

   .. ## pygame.event.wait ##

.. function:: peek

   | :sl:`test if event types are waiting on the queue`
   | :sg:`peek(eventtype=None) -> bool`
   | :sg:`peek(eventtype=None, pump=True) -> bool`

   Returns ``True`` if there are any events of the given type waiting on the
   queue. If a sequence of event types is passed, this will return ``True`` if
   any of those events are on the queue.

   When ``eventtype`` is not passed or ``None``, this function will return ``True`` if
   there's any event on the queue, and return ``False`` if the queue is empty.

   If ``pump`` is ``True`` (the default), then :func:`pygame.event.pump()` will be called.

   .. versionchangedold:: 1.9.5 Added ``pump`` argument

   .. versionchanged:: 2.5.3 no longer mistakenly returns an event when ``eventtype`` is None or not passed.

   .. ## pygame.event.peek ##

.. function:: clear

   | :sl:`remove all events from the queue`
   | :sg:`clear(eventtype=None) -> None`
   | :sg:`clear(eventtype=None, pump=True) -> None`

   Removes all events from the queue. If ``eventtype`` is given, removes the given event
   or sequence of events. This has the same effect as :func:`pygame.event.get()` except ``None``
   is returned. It can be slightly more efficient when clearing a full event queue.

   If ``pump`` is ``True`` (the default), then :func:`pygame.event.pump()` will be called.

   .. versionchangedold:: 1.9.5 Added ``pump`` argument

   .. ## pygame.event.clear ##

.. function:: event_name

   | :sl:`get the string name from an event id`
   | :sg:`event_name(type, /) -> string`

   Returns a string representing the name (in CapWords style) of the given
   event type.

   "UserEvent" is returned for all values in the user event id range.
   "Unknown" is returned when the event type does not exist.

   .. ## pygame.event.event_name ##

.. function:: set_blocked

   | :sl:`control which events are blocked on the queue`
   | :sg:`set_blocked(type, /) -> None`
   | :sg:`set_blocked(typelist, /) -> None`
   | :sg:`set_blocked(None) -> None`

   The given event types are not allowed to appear on the event queue. By
   default all events can be placed on the queue. It is safe to disable an
   event type multiple times.

   If ``None`` is passed as the argument, ALL of the event types are blocked
   from being placed on the queue.

   .. ## pygame.event.set_blocked ##

.. function:: set_allowed

   | :sl:`control which events are allowed on the queue`
   | :sg:`set_allowed(type, /) -> None`
   | :sg:`set_allowed(typelist, /) -> None`
   | :sg:`set_allowed(None) -> None`

   The given event types are allowed to appear on the event queue. By default,
   all event types can be placed on the queue. It is safe to enable an event
   type multiple times.

   If ``None`` is passed as the argument, ALL of the event types are allowed
   to be placed on the queue.

   .. ## pygame.event.set_allowed ##

.. function:: get_blocked

   | :sl:`test if a type of event is blocked from the queue`
   | :sg:`get_blocked(type, /) -> bool`
   | :sg:`get_blocked(typelist, /) -> bool`

   Returns ``True`` if the given event type is blocked from the queue. If a
   sequence of event types is passed, this will return ``True`` if any of those
   event types are blocked.

   .. ## pygame.event.get_blocked ##

.. function:: set_grab

   | :sl:`control the sharing of input devices with other applications`
   | :sg:`set_grab(bool, /) -> None`

   When your program runs in a windowed environment, it will share the mouse
   and keyboard devices with other applications that have focus. If your
   program sets the event grab to ``True``, it will lock all input into your
   program.

   It is best to not always grab the input, since it prevents the user from
   doing other things on their system.

   .. ## pygame.event.set_grab ##

.. function:: get_grab

   | :sl:`test if the program is sharing input devices`
   | :sg:`get_grab() -> bool`

   Returns ``True`` when the input events are grabbed for this application.

   .. ## pygame.event.get_grab ##

.. function:: post

   | :sl:`place a new event on the queue`
   | :sg:`post(event, /) -> bool`

   Places the given event at the end of the event queue.

   This is usually used for placing custom events on the event queue.
   Any type of event can be posted, and the events posted can have any attributes.

   When this event is received on the event queue, it will be a shallow copy of
   the event object posted by this function; the dict attribute of both events
   will be a reference to the same dict object in memory. Modifications on one
   dict can affect another, use deepcopy operations on the dict object if you
   don't want this behaviour.

   This returns a boolean on whether the event was posted or not. Blocked events
   cannot be posted, and this function returns ``False`` if you try to post them.

   .. versionchangedold:: 2.0.1 returns a boolean, previously returned ``None``

   .. ## pygame.event.post ##

.. function:: custom_type

   | :sl:`make custom user event type`
   | :sg:`custom_type() -> int`

   Reserves an event slot for use in a custom event ``userevent`` and returns the integer that the event slot is reserved to.

   If too many events are made a :exc:`pygame.error` is raised.

   .. versionaddedold:: 2.0.0.dev3

   .. ## pygame.event.custom_type ##

.. class:: Event

   | :sl:`pygame object for representing events`
   | :sg:`Event(type, dict) -> Event`
   | :sg:`Event(type, \**attributes) -> Event`

   A pygame object used for representing an event. ``Event`` instances
   support attribute assignment and deletion.

   When creating the object, the attributes may come from a dictionary
   argument with string keys or from keyword arguments.

   .. versionchanged:: 2.1.4 This class is also available through the ``pygame.Event``
      alias.

   .. note::
      From version 2.1.3 ``EventType`` is an alias for ``Event``. Beforehand,
      ``Event`` was a function that returned ``EventType`` instances. Use of
      ``Event`` is preferred over ``EventType`` wherever it is possible, as
      the latter could be deprecated in a future version.

   .. attribute:: type

      | :sl:`event type identifier.`
      | :sg:`type -> int`

      Read-only. The event type identifier. For user created event
      objects, this is the ``type`` argument passed to
      :class:`pygame.event.Event()`.

      For example, some predefined event identifiers are ``QUIT`` and
      ``MOUSEMOTION``.

      .. ## pygame.event.Event.type ##

   .. attribute:: __dict__

      | :sl:`event attribute dictionary`
      | :sg:`__dict__ -> dict`

      Read-only. The event type specific attributes of an event. The
      ``dict`` attribute is a synonym for backward compatibility.

      For example, the attributes of a ``KEYDOWN`` event would be ``unicode``,
      ``key``, and ``mod``

      .. ## pygame.event.Event.__dict__ ##

   .. versionaddedold:: 1.9.2 Mutable attributes.

   .. ## pygame.event.Event ##

.. ## pygame.event ##
