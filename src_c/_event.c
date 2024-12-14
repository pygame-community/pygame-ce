/*
  pygame-ce - Python Game Library
  Copyright (C) 2000-2001  Pete Shinners

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Library General Public
  License as published by the Free Software Foundation; either
  version 2 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Library General Public License for more details.

  You should have received a copy of the GNU Library General Public
  License along with this library; if not, write to the Free
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

  Pete Shinners
  pete@shinners.org
*/

/*
 *  pygame event module
 */
#define PYGAMEAPI_EVENT_INTERNAL

#include "pygame.h"

#include "pgcompat.h"

#include "doc/event_doc.h"

#ifndef PG_SDL3
// The system message code is only tested on windows, so only
//   include it there for now.
#include <SDL_syswm.h>
#endif

#define JOYEVENT_INSTANCE_ID "instance_id"
#define JOYEVENT_DEVICE_INDEX "device_index"

/* Define custom functions for peep events, for SDL1/2 compat */
#define PG_PEEP_EVENT(a, b, c, d) SDL_PeepEvents(a, b, c, d, d)
#define PG_PEEP_EVENT_ALL(x, y, z) \
    SDL_PeepEvents(x, y, z, SDL_FIRSTEVENT, SDL_LASTEVENT)

#define MAX_UINT32 0xFFFFFFFF

#define PG_GET_LIST_LEN 128

static int _pg_event_is_init = 0;

/* Length of our unicode string in bytes. We need 1 to 3 bytes to store
 * our unicode data, so we use a length of 4, to include the NULL byte
 * at the end as well */
#define UNICODE_LEN 4

/* This defines the maximum values of key-press and unicode values we
 * can store at a time, it is used for determining the unicode attribute
 * for KEYUP events. Now that its set to 15, it means that a user can
 * simultaneously hold 15 keys (who would do that?) and on release, all
 * KEYUP events will have unicode attribute. Why 15? You can set any
 * arbitrary number you like ;) */
#define MAX_SCAN_UNICODE 15

/* SDL mutex to be held in the event filter when global state is modified.
 * This mutex is intentionally immortalised (never freed during the entire
 * duration of the program) because its cleanup can be messy with multiple
 * threads trying to use it. Since it's a singleton we don't need to worry
 * about memory leaks */
#ifndef __EMSCRIPTEN__
/* emscripten does not allow multithreading for now and SDL_CreateMutex fails.
 * Don't bother with mutexes on emscripten for now */
static SDL_mutex *pg_evfilter_mutex = NULL;
#endif

static struct ScanAndUnicode {
    SDL_Scancode key;
    char unicode[UNICODE_LEN];
} scanunicode[MAX_SCAN_UNICODE] = {{0}};

static int pg_key_repeat_delay = 0;
static int pg_key_repeat_interval = 0;

static SDL_TimerID _pg_repeat_timer = 0;
static SDL_Event _pg_repeat_event;
static SDL_Event _pg_last_keydown_event = {0};

#define INPUT_BUFFER_SIZE SDL_NUM_SCANCODES + SDL_NUM_SCANCODES + 5 + 5
#define INPUT_BUFFER_PRESSED_OFFSET 0
#define INPUT_BUFFER_RELEASED_OFFSET \
    INPUT_BUFFER_PRESSED_OFFSET + SDL_NUM_SCANCODES
#define INPUT_BUFFER_MOUSE_PRESSED_OFFSET \
    INPUT_BUFFER_RELEASED_OFFSET + SDL_NUM_SCANCODES
#define INPUT_BUFFER_MOUSE_RELEASED_OFFSET \
    INPUT_BUFFER_MOUSE_PRESSED_OFFSET + 5

static_assert(INPUT_BUFFER_MOUSE_RELEASED_OFFSET + 5 == INPUT_BUFFER_SIZE,
              "mismatched buffer ranges definition");

/* Not used as text, acts as an array of bools */
static char input_buffer[INPUT_BUFFER_SIZE] = {0};

static PyObject *_event_class = NULL;

#ifdef __EMSCRIPTEN__
/* these macros are no-op here */
#define PG_LOCK_EVFILTER_MUTEX
#define PG_UNLOCK_EVFILTER_MUTEX
#else /* not on emscripten */

#define PG_LOCK_EVFILTER_MUTEX                                             \
    if (pg_evfilter_mutex) {                                               \
        if (PG_LockMutex(pg_evfilter_mutex) < 0) {                         \
            /* TODO: better error handling with future error-event API */  \
            /* since this error is very rare, we can completely give up if \
             * this happens for now */                                     \
            printf("Fatal pygame error in SDL_LockMutex: %s",              \
                   SDL_GetError());                                        \
            PG_EXIT(1);                                                    \
        }                                                                  \
    }

#define PG_UNLOCK_EVFILTER_MUTEX                                           \
    if (pg_evfilter_mutex) {                                               \
        if (PG_UnlockMutex(pg_evfilter_mutex) < 0) {                       \
            /* TODO: handle errors with future error-event API */          \
            /* since this error is very rare, we can completely give up if \
             * this happens for now */                                     \
            printf("Fatal pygame error in SDL_UnlockMutex: %s",            \
                   SDL_GetError());                                        \
            PG_EXIT(1);                                                    \
        }                                                                  \
    }
#endif /* not on emscripten */

#if SDL_VERSION_ATLEAST(3, 0, 0)
static Uint32
_pg_repeat_callback(void *param, SDL_TimerID timerID, Uint32 interval)
#else
static Uint32
_pg_repeat_callback(Uint32 interval, void *param)
#endif
{
    /* This function is called in a SDL Timer thread */
    PG_LOCK_EVFILTER_MUTEX
    /* This assignment only shallow-copies, but SDL_KeyboardEvent does not have
     * any pointer values so it's safe to do */
    SDL_Event repeat_event_copy = _pg_repeat_event;
    int repeat_interval_copy = pg_key_repeat_interval;
    PG_UNLOCK_EVFILTER_MUTEX

    repeat_event_copy.type = PGE_KEYREPEAT;
#if SDL_VERSION_ATLEAST(3, 0, 0)
    repeat_event_copy.key.down = true;
    repeat_event_copy.key.repeat = true;
#else
    repeat_event_copy.key.state = SDL_PRESSED;
    repeat_event_copy.key.repeat = 1;
#endif
    SDL_PushEvent(&repeat_event_copy);
    return repeat_interval_copy;
}

/* This function attempts to determine the unicode attribute from
 * the keydown/keyup event. This is used as a last-resort, in case we
 * could not determine the unicode from TEXTINPUT field. Why?
 * Because this function is really basic and cannot determine the
 * fancy unicode characters, just the basic ones
 *
 * One more advantage of this function is that it can return unicode
 * for some keys which TEXTINPUT does not provide (which unicode
 * attribute of SDL1 provided) */
static char
_pg_unicode_from_event(SDL_Event *event)
{
#if SDL_VERSION_ATLEAST(3, 0, 0)
    int capsheld = event->key.mod & KMOD_CAPS;
    int shiftheld = event->key.mod & KMOD_SHIFT;
    SDL_Keycode key = event->key.key;
#else
    int capsheld = event->key.keysym.mod & KMOD_CAPS;
    int shiftheld = event->key.keysym.mod & KMOD_SHIFT;
    SDL_Keycode key = event->key.keysym.sym;
#endif
    int capitalize = (capsheld && !shiftheld) || (shiftheld && !capsheld);

#if SDL_VERSION_ATLEAST(3, 0, 0)
    if (event->key.mod & KMOD_CTRL)
#else
    if (event->key.keysym.mod & KMOD_CTRL)
#endif
    {
        /* Control Key held, send control-key related unicode. */
        if (key >= SDLK_a && key <= SDLK_z)
            return key - SDLK_a + 1;
        else {
            switch (key) {
                case SDLK_2:
                case SDLK_AT:
                    return '\0';
                case SDLK_3:
                case SDLK_LEFTBRACKET:
                    return '\x1b';
                case SDLK_4:
                case SDLK_BACKSLASH:
                    return '\x1c';
                case SDLK_5:
                case SDLK_RIGHTBRACKET:
                    return '\x1d';
                case SDLK_6:
                case SDLK_CARET:
                    return '\x1e';
                case SDLK_7:
                case SDLK_UNDERSCORE:
                    return '\x1f';
                case SDLK_8:
                    return '\x7f';
            }
        }
    }
    if (key < 128) {
        if (capitalize && key >= SDLK_a && key <= SDLK_z)
            return key + 'A' - 'a';
        return key;
    }

    switch (key) {
        case SDLK_KP_PERIOD:
            return '.';
        case SDLK_KP_DIVIDE:
            return '/';
        case SDLK_KP_MULTIPLY:
            return '*';
        case SDLK_KP_MINUS:
            return '-';
        case SDLK_KP_PLUS:
            return '+';
        case SDLK_KP_ENTER:
            return '\r';
        case SDLK_KP_EQUALS:
            return '=';
    }
    return '\0';
}

/* Strip a utf-8 encoded string to contain only first character. Also
 * ensure that character can be represented within 3 bytes, because SDL1
 * did not support unicode characters that took up 4 bytes. In case this
 * bit of code is not clear, here is a python equivalent
def _pg_strip_utf8(string):
    if chr(string[0]) <= 0xFFFF:
        return string[0]
    else:
        return ""
*/
static void
_pg_strip_utf8(const char *str, char *ret)
{
    Uint8 firstbyte = (Uint8)*str;

    /* Zero unicode buffer */
    memset(ret, 0, UNICODE_LEN);

    /* 1111 0000 is 0xF0 */
    if (firstbyte >= 0xF0) {
        /* Too large UTF8 string, do nothing */
        return;
    }

    /* 1110 0000 is 0xE0 */
    if (firstbyte >= 0xE0) {
        /* Copy first 3 bytes */
        memcpy(ret, str, 3);
    }
    /* 1100 0000 is 0xC0 */
    else if (firstbyte >= 0xC0) {
        /* Copy first 2 bytes */
        memcpy(ret, str, 2);
    }
    /* 1000 0000 is 0x80 */
    else if (firstbyte < 0x80) {
        /* Copy first byte */
        memcpy(ret, str, 1);
    }
}

static int
_pg_put_event_unicode(SDL_Event *event, const char *uni)
{
    int i;
    for (i = 0; i < MAX_SCAN_UNICODE; i++) {
        if (!scanunicode[i].key) {
#if SDL_VERSION_ATLEAST(3, 0, 0)
            scanunicode[i].key = event->key.scancode;
#else
            scanunicode[i].key = event->key.keysym.scancode;
#endif
            _pg_strip_utf8(uni, scanunicode[i].unicode);
            return 1;
        }
    }
    return 0;
}

static PyObject *
_pg_get_event_unicode(SDL_Event *event)
{
    /* We only deal with one byte here, but still declare an array to silence
     * compiler warnings. The other 3 bytes are unused */
    char c[4];
    int i;
    for (i = 0; i < MAX_SCAN_UNICODE; i++) {
#if SDL_VERSION_ATLEAST(3, 0, 0)
        if (scanunicode[i].key == event->key.scancode)
#else
        if (scanunicode[i].key == event->key.keysym.scancode)
#endif
        {
            if (event->type == SDL_KEYUP) {
                /* mark the position as free real estate for other
                 * events to occupy. */
                scanunicode[i].key = 0;
            }
            return PyUnicode_FromString(scanunicode[i].unicode);
        }
    }
    /* fallback to function that determines unicode from the event.
     * We try to get the unicode attribute, and store it in memory*/
    *c = _pg_unicode_from_event(event);
    if (_pg_put_event_unicode(event, c))
        return _pg_get_event_unicode(event);
    return PyUnicode_FromString("");
}

#define _PG_HANDLE_PROXIFY(name) \
    case SDL_##name:             \
    case PGPOST_##name:          \
        return proxify ? PGPOST_##name : SDL_##name

#define _PG_HANDLE_PROXIFY_PGE(name) \
    case PGE_##name:                 \
    case PGPOST_##name:              \
        return proxify ? PGPOST_##name : PGE_##name

/* The next three functions are used for proxying SDL events to and from
 * PGPOST_* events.
 *
 * Some SDL1 events (SDL_ACTIVEEVENT, SDL_VIDEORESIZE and SDL_VIDEOEXPOSE)
 * are redefined with SDL2, they HAVE to be proxied.
 *
 * SDL_USEREVENT is not proxied, because with SDL2, pygame assigns a
 * different event in place of SDL_USEREVENT, and users use PGE_USEREVENT
 *
 * Each WINDOW_* event must be defined twice, once as an event, and also
 * again, as a proxy event. WINDOW_* events MUST be proxied.
 */

static Uint32
_pg_pgevent_proxify_helper(Uint32 type, Uint8 proxify)
{
    switch (type) {
        _PG_HANDLE_PROXIFY(ACTIVEEVENT);
        _PG_HANDLE_PROXIFY(APP_TERMINATING);
        _PG_HANDLE_PROXIFY(APP_LOWMEMORY);
        _PG_HANDLE_PROXIFY(APP_WILLENTERBACKGROUND);
        _PG_HANDLE_PROXIFY(APP_DIDENTERBACKGROUND);
        _PG_HANDLE_PROXIFY(APP_WILLENTERFOREGROUND);
        _PG_HANDLE_PROXIFY(APP_DIDENTERFOREGROUND);
        _PG_HANDLE_PROXIFY(AUDIODEVICEADDED);
        _PG_HANDLE_PROXIFY(AUDIODEVICEREMOVED);
        _PG_HANDLE_PROXIFY(CLIPBOARDUPDATE);
        _PG_HANDLE_PROXIFY(CONTROLLERAXISMOTION);
        _PG_HANDLE_PROXIFY(CONTROLLERBUTTONDOWN);
        _PG_HANDLE_PROXIFY(CONTROLLERBUTTONUP);
        _PG_HANDLE_PROXIFY(CONTROLLERDEVICEADDED);
        _PG_HANDLE_PROXIFY(CONTROLLERDEVICEREMOVED);
        _PG_HANDLE_PROXIFY(CONTROLLERDEVICEREMAPPED);
        _PG_HANDLE_PROXIFY(CONTROLLERTOUCHPADDOWN);
        _PG_HANDLE_PROXIFY(CONTROLLERTOUCHPADMOTION);
        _PG_HANDLE_PROXIFY(CONTROLLERTOUCHPADUP);
        _PG_HANDLE_PROXIFY(CONTROLLERSENSORUPDATE);
#if !SDL_VERSION_ATLEAST(3, 0, 0)
        _PG_HANDLE_PROXIFY(DOLLARGESTURE);
        _PG_HANDLE_PROXIFY(DOLLARRECORD);
#endif
        _PG_HANDLE_PROXIFY(DROPFILE);
        _PG_HANDLE_PROXIFY(DROPTEXT);
        _PG_HANDLE_PROXIFY(DROPBEGIN);
        _PG_HANDLE_PROXIFY(DROPCOMPLETE);
        _PG_HANDLE_PROXIFY(FINGERMOTION);
        _PG_HANDLE_PROXIFY(FINGERDOWN);
        _PG_HANDLE_PROXIFY(FINGERUP);
        _PG_HANDLE_PROXIFY(KEYDOWN);
        _PG_HANDLE_PROXIFY(KEYUP);
        _PG_HANDLE_PROXIFY(KEYMAPCHANGED);
        _PG_HANDLE_PROXIFY(JOYAXISMOTION);
        _PG_HANDLE_PROXIFY(JOYBALLMOTION);
        _PG_HANDLE_PROXIFY(JOYHATMOTION);
        _PG_HANDLE_PROXIFY(JOYBUTTONDOWN);
        _PG_HANDLE_PROXIFY(JOYBUTTONUP);
        _PG_HANDLE_PROXIFY(JOYDEVICEADDED);
        _PG_HANDLE_PROXIFY(JOYDEVICEREMOVED);
        _PG_HANDLE_PROXIFY(LOCALECHANGED);
        _PG_HANDLE_PROXIFY(MOUSEMOTION);
        _PG_HANDLE_PROXIFY(MOUSEBUTTONDOWN);
        _PG_HANDLE_PROXIFY(MOUSEBUTTONUP);
        _PG_HANDLE_PROXIFY(MOUSEWHEEL);
#if !SDL_VERSION_ATLEAST(3, 0, 0)
        _PG_HANDLE_PROXIFY(MULTIGESTURE);
#endif
        _PG_HANDLE_PROXIFY(NOEVENT);
        _PG_HANDLE_PROXIFY(QUIT);
        _PG_HANDLE_PROXIFY(RENDER_TARGETS_RESET);
        _PG_HANDLE_PROXIFY(RENDER_DEVICE_RESET);
        _PG_HANDLE_PROXIFY(SYSWMEVENT);
        _PG_HANDLE_PROXIFY(TEXTEDITING);
        _PG_HANDLE_PROXIFY(TEXTINPUT);
        _PG_HANDLE_PROXIFY(VIDEORESIZE);
        _PG_HANDLE_PROXIFY(VIDEOEXPOSE);
        _PG_HANDLE_PROXIFY_PGE(MIDIIN);
        _PG_HANDLE_PROXIFY_PGE(MIDIOUT);
        _PG_HANDLE_PROXIFY_PGE(WINDOWSHOWN);
        _PG_HANDLE_PROXIFY_PGE(WINDOWHIDDEN);
        _PG_HANDLE_PROXIFY_PGE(WINDOWEXPOSED);
        _PG_HANDLE_PROXIFY_PGE(WINDOWMOVED);
        _PG_HANDLE_PROXIFY_PGE(WINDOWRESIZED);
        _PG_HANDLE_PROXIFY_PGE(WINDOWSIZECHANGED);
        _PG_HANDLE_PROXIFY_PGE(WINDOWMINIMIZED);
        _PG_HANDLE_PROXIFY_PGE(WINDOWMAXIMIZED);
        _PG_HANDLE_PROXIFY_PGE(WINDOWRESTORED);
        _PG_HANDLE_PROXIFY_PGE(WINDOWENTER);
        _PG_HANDLE_PROXIFY_PGE(WINDOWLEAVE);
        _PG_HANDLE_PROXIFY_PGE(WINDOWFOCUSGAINED);
        _PG_HANDLE_PROXIFY_PGE(WINDOWFOCUSLOST);
        _PG_HANDLE_PROXIFY_PGE(WINDOWCLOSE);
        _PG_HANDLE_PROXIFY_PGE(WINDOWTAKEFOCUS);
        _PG_HANDLE_PROXIFY_PGE(WINDOWHITTEST);
        _PG_HANDLE_PROXIFY_PGE(WINDOWICCPROFCHANGED);
        _PG_HANDLE_PROXIFY_PGE(WINDOWDISPLAYCHANGED);
        default:
            return type;
    }
}

static Uint32
_pg_pgevent_proxify(Uint32 type)
{
    return _pg_pgevent_proxify_helper(type, 1);
}

static Uint32
_pg_pgevent_deproxify(Uint32 type)
{
    return _pg_pgevent_proxify_helper(type, 0);
}

#if !SDL_VERSION_ATLEAST(3, 0, 0)
/* We don't need to do window event translation because in SDL3 each window
 * event is its own thing anyways */
static int
_pg_translate_windowevent(void *_, SDL_Event *event)
{
    if (event->type == SDL_WINDOWEVENT) {
        event->type = PGE_WINDOWSHOWN + event->window.event - 1;
        return PG_EventEnabled(_pg_pgevent_proxify(event->type));
    }
    return 1;
}
#endif

#if SDL_VERSION_ATLEAST(3, 0, 0)
static bool SDLCALL
#else
static int SDLCALL
#endif
_pg_remove_pending_VIDEORESIZE(void *userdata, SDL_Event *event)
{
    SDL_Event *new_event = (SDL_Event *)userdata;

    if (event->type == SDL_VIDEORESIZE &&
        event->window.windowID == new_event->window.windowID) {
        /* We're about to post a new size event, drop the old ones */
        return 0;
    }
    return 1;
}

#if SDL_VERSION_ATLEAST(3, 0, 0)
static bool SDLCALL
#else
static int SDLCALL
#endif
_pg_remove_pending_VIDEOEXPOSE(void *userdata, SDL_Event *event)
{
    SDL_Event *new_event = (SDL_Event *)userdata;

    if (event->type == SDL_VIDEOEXPOSE &&
        event->window.windowID == new_event->window.windowID) {
        /* We're about to post a new videoexpose event, drop the old ones */
        return 0;
    }
    return 1;
}

/* SDL 2 to SDL 1.2 event mapping and SDL 1.2 key repeat emulation,
 * this can alter events in-place.
 * This function can be called from multiple threads, so a mutex must be held
 * when this function tries to modify any global state (the mutex is not needed
 * on all branches of this function) */
#if SDL_VERSION_ATLEAST(3, 0, 0)
static bool SDLCALL
#else
static int SDLCALL
#endif
pg_event_filter(void *_, SDL_Event *event)
{
    SDL_Event newdownevent, newupevent, newevent = *event;
#if SDL_VERSION_ATLEAST(3, 0, 0)
    float x, y;
    int i;
#else
    int x, y, i;
#endif

#if SDL_VERSION_ATLEAST(3, 0, 0)
    if (event->type >= SDL_EVENT_WINDOW_FIRST &&
        event->type <= SDL_EVENT_WINDOW_LAST)
#else
    if (event->type == SDL_WINDOWEVENT)
#endif
    {
        /* DON'T filter SDL_WINDOWEVENTs here. If we delete events, they
         * won't be available to low-level SDL2 either.*/
        switch (
#if SDL_VERSION_ATLEAST(3, 0, 0)
            event->type
#else
            event->window.event
#endif
        ) {
            case SDL_WINDOWEVENT_RESIZED:
                SDL_FilterEvents(_pg_remove_pending_VIDEORESIZE, &newevent);

                newevent.type = SDL_VIDEORESIZE;
                SDL_PushEvent(&newevent);
                break;
            case SDL_WINDOWEVENT_EXPOSED:
                SDL_FilterEvents(_pg_remove_pending_VIDEOEXPOSE, &newevent);

                newevent.type = SDL_VIDEOEXPOSE;
                SDL_PushEvent(&newevent);
                break;
            case SDL_WINDOWEVENT_ENTER:
            case SDL_WINDOWEVENT_LEAVE:
            case SDL_WINDOWEVENT_FOCUS_GAINED:
            case SDL_WINDOWEVENT_FOCUS_LOST:
            case SDL_WINDOWEVENT_MINIMIZED:
            case SDL_WINDOWEVENT_RESTORED:
                newevent.type = SDL_ACTIVEEVENT;
#if SDL_VERSION_ATLEAST(3, 0, 0)
                /* Backup event->type because it is needed later */
                newevent.window.data2 = event->type;
#endif
                SDL_PushEvent(&newevent);
        }
    }

    else if (event->type == SDL_KEYDOWN) {
        if (event->key.repeat)
            return 0;

        PG_LOCK_EVFILTER_MUTEX
#if SDL_VERSION_ATLEAST(3, 0, 0)
        input_buffer[INPUT_BUFFER_PRESSED_OFFSET + event->key.scancode] = 1;
#else
        input_buffer[INPUT_BUFFER_PRESSED_OFFSET +
                     event->key.keysym.scancode] = 1;
#endif
        if (pg_key_repeat_delay > 0) {
            if (_pg_repeat_timer)
                SDL_RemoveTimer(_pg_repeat_timer);

            _pg_repeat_event = *event;
            _pg_repeat_timer =
                SDL_AddTimer(pg_key_repeat_delay, _pg_repeat_callback, NULL);
        }

        /* store the keydown event for later in the SDL_TEXTINPUT */
        _pg_last_keydown_event = *event;
        PG_UNLOCK_EVFILTER_MUTEX
    }

    else if (event->type == SDL_TEXTINPUT) {
        PG_LOCK_EVFILTER_MUTEX
        if (_pg_last_keydown_event.type) {
            _pg_put_event_unicode(&_pg_last_keydown_event, event->text.text);
            _pg_last_keydown_event.type = 0;
        }
        PG_UNLOCK_EVFILTER_MUTEX
    }

    else if (event->type == PGE_KEYREPEAT) {
        event->type = SDL_KEYDOWN;
    }

    else if (event->type == SDL_KEYUP) {
        PG_LOCK_EVFILTER_MUTEX
#if SDL_VERSION_ATLEAST(3, 0, 0)
        input_buffer[INPUT_BUFFER_RELEASED_OFFSET + event->key.scancode] = 1;
        if (_pg_repeat_timer &&
            _pg_repeat_event.key.scancode == event->key.scancode)
#else
        input_buffer[INPUT_BUFFER_RELEASED_OFFSET +
                     event->key.keysym.scancode] = 1;
        if (_pg_repeat_timer &&
            _pg_repeat_event.key.keysym.scancode == event->key.keysym.scancode)
#endif
        {
            SDL_RemoveTimer(_pg_repeat_timer);
            _pg_repeat_timer = 0;
        }
        PG_UNLOCK_EVFILTER_MUTEX
    }

    else if (event->type == SDL_MOUSEBUTTONDOWN ||
             event->type == SDL_MOUSEBUTTONUP) {
        if (event->type == SDL_MOUSEBUTTONDOWN &&
            event->button.button - 1 < 5) {
            input_buffer[INPUT_BUFFER_MOUSE_PRESSED_OFFSET +
                         event->button.button - 1] = 1;
        }
        else if (event->type == SDL_MOUSEBUTTONUP &&
                 event->button.button - 1 < 5) {
            input_buffer[INPUT_BUFFER_MOUSE_RELEASED_OFFSET +
                         event->button.button - 1] = 1;
        }
        if (event->button.button & PGM_BUTTON_KEEP)
            event->button.button ^= PGM_BUTTON_KEEP;
        else if (event->button.button >= PGM_BUTTON_WHEELUP)
            event->button.button += (PGM_BUTTON_X1 - PGM_BUTTON_WHEELUP);
    }

    else if (event->type == SDL_MOUSEWHEEL) {
        // #691 We are not moving wheel!
        if (!event->wheel.y && !event->wheel.x)
            return 0;

        SDL_GetMouseState(&x, &y);
        /* Generate a MouseButtonDown event and MouseButtonUp for
         * compatibility. https://wiki.libsdl.org/SDL_MouseWheelEvent
         */
        newdownevent.type = SDL_MOUSEBUTTONDOWN;
        newdownevent.button.x = x;
        newdownevent.button.y = y;
#if SDL_VERSION_ATLEAST(3, 0, 0)
        newdownevent.button.down = true;
#else
        newdownevent.button.state = SDL_PRESSED;
#endif
        newdownevent.button.clicks = 1;
        newdownevent.button.which = event->button.which;

        newupevent.type = SDL_MOUSEBUTTONUP;
        newupevent.button.x = x;
        newupevent.button.y = y;
#if SDL_VERSION_ATLEAST(3, 0, 0)
        newupevent.button.down = false;
#else
        newupevent.button.state = SDL_RELEASED;
#endif
        newupevent.button.clicks = 1;
        newupevent.button.which = event->button.which;

        /* Use a for loop to simulate multiple events, because SDL 1
         * works that way */
        for (i = 0; i < abs((int)event->wheel.y); i++) {
            /* Do this in the loop because button.button is mutated before it
             * is posted from this filter */
            if (event->wheel.y > 0) {
                newdownevent.button.button = newupevent.button.button =
                    PGM_BUTTON_WHEELUP | PGM_BUTTON_KEEP;
            }
            else {
                newdownevent.button.button = newupevent.button.button =
                    PGM_BUTTON_WHEELDOWN | PGM_BUTTON_KEEP;
            }
            SDL_PushEvent(&newdownevent);
            SDL_PushEvent(&newupevent);
        }
        /* this doesn't work! This is called by SDL, not Python:
          if (SDL_PushEvent(&newdownevent) < 0)
            return RAISE(pgExc_SDLError, SDL_GetError()), 0;
        */
    }
    return PG_EventEnabled(_pg_pgevent_proxify(event->type));
}

/* The two keyrepeat functions below modify state accessed by the event filter,
 * so they too need to hold the safety mutex */
static int
pg_EnableKeyRepeat(int delay, int interval)
{
    if (delay < 0 || interval < 0) {
        PyErr_SetString(PyExc_ValueError,
                        "delay and interval must equal at least 0");
        return -1;
    }
    PG_LOCK_EVFILTER_MUTEX
    pg_key_repeat_delay = delay;
    pg_key_repeat_interval = interval;
    PG_UNLOCK_EVFILTER_MUTEX
    return 0;
}

static void
pg_GetKeyRepeat(int *delay, int *interval)
{
    PG_LOCK_EVFILTER_MUTEX
    *delay = pg_key_repeat_delay;
    *interval = pg_key_repeat_interval;
    PG_UNLOCK_EVFILTER_MUTEX
}

static PyObject *
pgEvent_AutoQuit(PyObject *self, PyObject *_null)
{
    if (_pg_event_is_init) {
        PG_LOCK_EVFILTER_MUTEX
        if (_pg_repeat_timer) {
            SDL_RemoveTimer(_pg_repeat_timer);
            _pg_repeat_timer = 0;
        }
        PG_UNLOCK_EVFILTER_MUTEX
    }
    _pg_event_is_init = 0;
    Py_RETURN_NONE;
}

static PyObject *
pgEvent_AutoInit(PyObject *self, PyObject *_null)
{
    if (!_pg_event_is_init) {
        pg_key_repeat_delay = 0;
        pg_key_repeat_interval = 0;
#ifndef __EMSCRIPTEN__
        if (!pg_evfilter_mutex) {
            /* Create mutex only if it has not been created already */
            pg_evfilter_mutex = SDL_CreateMutex();
            if (!pg_evfilter_mutex)
                return RAISE(pgExc_SDLError, SDL_GetError());
        }
#endif
        SDL_SetEventFilter(pg_event_filter, NULL);
    }
    _pg_event_is_init = 1;
    Py_RETURN_NONE;
}

/* Similar to pg_post_event, but it steals the reference to obj and does not
 * need GIL to be held at all.*/
static int
pg_post_event_steal(int type, PyObject *obj)
{
    SDL_Event event = {0};
    event.type = _pg_pgevent_proxify(type);
    event.user.data1 = (void *)obj;
    return SDL_PushEvent(&event);
}

/* This function posts an SDL "UserEvent" event, can also optionally take a
 * dict or an Event instance. This function does not need GIL to be held if obj
 * is NULL, but needs GIL otherwise
 */
static int
pg_post_event(int type, PyObject *obj)
{
    if (obj)
        Py_INCREF(obj);

    int ret = pg_post_event_steal(type, obj);

    if (ret != 1 && obj)
        Py_DECREF(obj);

    return ret;
}

/* Helper for adding objects to dictionaries. Check for errors with
   PyErr_Occurred() */
static void
_pg_insobj(PyObject *dict, char *name, PyObject *v)
{
    if (v) {
        PyDict_SetItemString(dict, name, v);
        Py_DECREF(v);
    }
}

#if SDL_VERSION_ATLEAST(3, 0, 0)
static PyObject *
get_joy_guid(SDL_JoystickID instance_id)
{
    char strguid[33];
    SDL_GUID guid = SDL_GetJoystickGUIDForID(instance_id);

    SDL_GUIDToString(guid, strguid, 33);
    return PyUnicode_FromString(strguid);
}
#else
static PyObject *
get_joy_guid(int device_index)
{
    char strguid[33];
    SDL_JoystickGUID guid = SDL_JoystickGetDeviceGUID(device_index);

    SDL_JoystickGetGUIDString(guid, strguid, 33);
    return PyUnicode_FromString(strguid);
}
#endif

static PyObject *
get_joy_device_index(int instance_id)
{
    int device_index = pgJoystick_GetDeviceIndexByInstanceID(instance_id);
    return PyLong_FromLong(device_index);
}

static PyObject *
dict_or_obj_from_event(SDL_Event *event)
{
    PyObject *dict = NULL, *tuple, *obj;
    int hx, hy;
    long gain;
    long state;

    /* check if a proxy event or userevent was posted */
    if (event->type >= PGPOST_EVENTBEGIN) {
        // This steals reference to obj from SDL_Event.
        return (PyObject *)event->user.data1;
    }

    dict = PyDict_New();
    if (!dict)
        return NULL;

    switch (event->type) {
        case SDL_VIDEORESIZE:
            obj = pg_tuple_couple_from_values_int(event->window.data1,
                                                  event->window.data2);
            _pg_insobj(dict, "size", obj);
            _pg_insobj(dict, "w", PyLong_FromLong(event->window.data1));
            _pg_insobj(dict, "h", PyLong_FromLong(event->window.data2));
            break;
        case SDL_ACTIVEEVENT:
#if SDL_VERSION_ATLEAST(3, 0, 0)
            switch (event->window.data2)
#else
            switch (event->window.event)
#endif
            {
                case SDL_WINDOWEVENT_ENTER:
                    gain = 1;
                    state = SDL_APPMOUSEFOCUS;
                    break;
                case SDL_WINDOWEVENT_LEAVE:
                    gain = 0;
                    state = SDL_APPMOUSEFOCUS;
                    break;
                case SDL_WINDOWEVENT_FOCUS_GAINED:
                    gain = 1;
                    state = SDL_APPINPUTFOCUS;
                    break;
                case SDL_WINDOWEVENT_FOCUS_LOST:
                    gain = 0;
                    state = SDL_APPINPUTFOCUS;
                    break;
                case SDL_WINDOWEVENT_MINIMIZED:
                    gain = 0;
                    state = SDL_APPACTIVE;
                    break;
                default:
                    assert(event->window.event == SDL_WINDOWEVENT_RESTORED);
                    gain = 1;
                    state = SDL_APPACTIVE;
            }
            _pg_insobj(dict, "gain", PyLong_FromLong(gain));
            _pg_insobj(dict, "state", PyLong_FromLong(state));
            break;
        case SDL_KEYDOWN:
        case SDL_KEYUP:
            PG_LOCK_EVFILTER_MUTEX
            /* this accesses state also accessed the event filter, so lock */
            _pg_insobj(dict, "unicode", _pg_get_event_unicode(event));
            PG_UNLOCK_EVFILTER_MUTEX
#if SDL_VERSION_ATLEAST(3, 0, 0)
            _pg_insobj(dict, "key", PyLong_FromLong(event->key.key));
            _pg_insobj(dict, "mod", PyLong_FromLong(event->key.mod));
            _pg_insobj(dict, "scancode", PyLong_FromLong(event->key.scancode));
#else
            _pg_insobj(dict, "key", PyLong_FromLong(event->key.keysym.sym));
            _pg_insobj(dict, "mod", PyLong_FromLong(event->key.keysym.mod));
            _pg_insobj(dict, "scancode",
                       PyLong_FromLong(event->key.keysym.scancode));
#endif
            break;
        case SDL_MOUSEMOTION:
            obj = pg_tuple_couple_from_values_int((int)event->motion.x,
                                                  (int)event->motion.y);
            _pg_insobj(dict, "pos", obj);
            obj = pg_tuple_couple_from_values_int((int)event->motion.xrel,
                                                  (int)event->motion.yrel);
            _pg_insobj(dict, "rel", obj);
            if ((tuple = PyTuple_New(3))) {
                PyTuple_SET_ITEM(tuple, 0,
                                 PyLong_FromLong((event->motion.state &
                                                  SDL_BUTTON(1)) != 0));
                PyTuple_SET_ITEM(tuple, 1,
                                 PyLong_FromLong((event->motion.state &
                                                  SDL_BUTTON(2)) != 0));
                PyTuple_SET_ITEM(tuple, 2,
                                 PyLong_FromLong((event->motion.state &
                                                  SDL_BUTTON(3)) != 0));
                _pg_insobj(dict, "buttons", tuple);
            }
            _pg_insobj(
                dict, "touch",
                PyBool_FromLong((event->motion.which == SDL_TOUCH_MOUSEID)));
            break;
        case SDL_MOUSEBUTTONDOWN:
        case SDL_MOUSEBUTTONUP:
            obj = pg_tuple_couple_from_values_int((int)event->button.x,
                                                  (int)event->button.y);
            _pg_insobj(dict, "pos", obj);
            _pg_insobj(dict, "button", PyLong_FromLong(event->button.button));
            _pg_insobj(
                dict, "touch",
                PyBool_FromLong((event->button.which == SDL_TOUCH_MOUSEID)));
            break;
        case SDL_JOYAXISMOTION:
            _pg_insobj(dict, "joy", get_joy_device_index(event->jaxis.which));
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->jaxis.which));
            _pg_insobj(dict, "axis", PyLong_FromLong(event->jaxis.axis));
            // sdl report axis values as values between -32768 and 32767
            _pg_insobj(dict, "value",
                       PyFloat_FromDouble(event->jaxis.value / 32768.0));
            break;
        case SDL_JOYBALLMOTION:
            _pg_insobj(dict, "joy", get_joy_device_index(event->jaxis.which));
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->jball.which));
            _pg_insobj(dict, "ball", PyLong_FromLong(event->jball.ball));
            obj = pg_tuple_couple_from_values_int(event->jball.xrel,
                                                  event->jball.yrel);
            _pg_insobj(dict, "rel", obj);
            break;
        case SDL_JOYHATMOTION:
            _pg_insobj(dict, "joy", get_joy_device_index(event->jaxis.which));
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->jhat.which));
            _pg_insobj(dict, "hat", PyLong_FromLong(event->jhat.hat));
            hx = hy = 0;
            if (event->jhat.value & SDL_HAT_UP)
                hy = 1;
            else if (event->jhat.value & SDL_HAT_DOWN)
                hy = -1;
            if (event->jhat.value & SDL_HAT_RIGHT)
                hx = 1;
            else if (event->jhat.value & SDL_HAT_LEFT)
                hx = -1;
            _pg_insobj(dict, "value", pg_tuple_couple_from_values_int(hx, hy));
            break;
        case SDL_JOYBUTTONUP:
        case SDL_JOYBUTTONDOWN:
            _pg_insobj(dict, "joy", get_joy_device_index(event->jaxis.which));
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->jbutton.which));
            _pg_insobj(dict, "button", PyLong_FromLong(event->jbutton.button));
            break;
        case PGE_WINDOWDISPLAYCHANGED:
            _pg_insobj(dict, "display_index",
                       PyLong_FromLong(event->window.data1));
        case PGE_WINDOWMOVED:
        case PGE_WINDOWRESIZED:
        case PGE_WINDOWSIZECHANGED:
            /*other PGE_WINDOW* events do not have attributes */
            _pg_insobj(dict, "x", PyLong_FromLong(event->window.data1));
            _pg_insobj(dict, "y", PyLong_FromLong(event->window.data2));
            break;
        case SDL_AUDIODEVICEADDED:
        case SDL_AUDIODEVICEREMOVED:
            _pg_insobj(
                dict, "which",
                PyLong_FromLong(
                    event->adevice
                        .which));  // The audio device index for the ADDED
                                   // event (valid until next
                                   // SDL_GetNumAudioDevices() call),
                                   // SDL_AudioDeviceID for the REMOVED event
#if SDL_VERSION_ATLEAST(3, 0, 0)
            _pg_insobj(dict, "iscapture",
                       PyLong_FromLong(event->adevice.recording));
#else
            _pg_insobj(dict, "iscapture",
                       PyLong_FromLong(event->adevice.iscapture));
#endif
            break;
        case SDL_FINGERMOTION:
        case SDL_FINGERDOWN:
        case SDL_FINGERUP:
            /* https://wiki.libsdl.org/SDL_TouchFingerEvent */
#if SDL_VERSION_ATLEAST(3, 0, 0)
            _pg_insobj(dict, "touch_id",
                       PyLong_FromLongLong(event->tfinger.touchID));
            _pg_insobj(dict, "finger_id",
                       PyLong_FromLongLong(event->tfinger.fingerID));
#else
            _pg_insobj(dict, "touch_id",
                       PyLong_FromLongLong(event->tfinger.touchId));
            _pg_insobj(dict, "finger_id",
                       PyLong_FromLongLong(event->tfinger.fingerId));
#endif
            _pg_insobj(dict, "x", PyFloat_FromDouble(event->tfinger.x));
            _pg_insobj(dict, "y", PyFloat_FromDouble(event->tfinger.y));
            _pg_insobj(dict, "dx", PyFloat_FromDouble(event->tfinger.dx));
            _pg_insobj(dict, "dy", PyFloat_FromDouble(event->tfinger.dy));
            _pg_insobj(dict, "pressure",
                       PyFloat_FromDouble(event->tfinger.dy));
            break;
#if !SDL_VERSION_ATLEAST(3, 0, 0)
        case SDL_MULTIGESTURE:
            /* https://wiki.libsdl.org/SDL_MultiGestureEvent */
            _pg_insobj(dict, "touch_id",
                       PyLong_FromLongLong(event->mgesture.touchId));
            _pg_insobj(dict, "x", PyFloat_FromDouble(event->mgesture.x));
            _pg_insobj(dict, "y", PyFloat_FromDouble(event->mgesture.y));
            _pg_insobj(dict, "rotated",
                       PyFloat_FromDouble(event->mgesture.dTheta));
            _pg_insobj(dict, "pinched",
                       PyFloat_FromDouble(event->mgesture.dDist));
            _pg_insobj(dict, "num_fingers",
                       PyLong_FromLong(event->mgesture.numFingers));
            break;
#endif
        case SDL_MOUSEWHEEL:
            /* https://wiki.libsdl.org/SDL_MouseWheelEvent */
#ifndef NO_SDL_MOUSEWHEEL_FLIPPED
            _pg_insobj(dict, "flipped",
                       PyBool_FromLong(event->wheel.direction ==
                                       SDL_MOUSEWHEEL_FLIPPED));
#else
            _pg_insobj(dict, "flipped", PyBool_FromLong(0));
#endif
            _pg_insobj(dict, "x", PyLong_FromLong((long)event->wheel.x));
            _pg_insobj(dict, "y", PyLong_FromLong((long)event->wheel.y));

#if SDL_VERSION_ATLEAST(3, 0, 0)
            _pg_insobj(dict, "precise_x",
                       PyFloat_FromDouble((double)event->wheel.x));
            _pg_insobj(dict, "precise_y",
                       PyFloat_FromDouble((double)event->wheel.y));
#elif SDL_VERSION_ATLEAST(2, 0, 18)
            _pg_insobj(dict, "precise_x",
                       PyFloat_FromDouble((double)event->wheel.preciseX));
            _pg_insobj(dict, "precise_y",
                       PyFloat_FromDouble((double)event->wheel.preciseY));

#else /* ~SDL_VERSION_ATLEAST(2, 0, 18) */
            /* fallback to regular x and y when SDL version used does not
             * support precise fields */
            _pg_insobj(dict, "precise_x",
                       PyFloat_FromDouble((double)event->wheel.x));
            _pg_insobj(dict, "precise_y",
                       PyFloat_FromDouble((double)event->wheel.y));

#endif /* ~SDL_VERSION_ATLEAST(2, 0, 18) */
            _pg_insobj(
                dict, "touch",
                PyBool_FromLong((event->wheel.which == SDL_TOUCH_MOUSEID)));

            break;
        case SDL_TEXTINPUT:
            /* https://wiki.libsdl.org/SDL_TextInputEvent */
            _pg_insobj(dict, "text", PyUnicode_FromString(event->text.text));
            break;
        case SDL_TEXTEDITING:
            /* https://wiki.libsdl.org/SDL_TextEditingEvent */
            _pg_insobj(dict, "text", PyUnicode_FromString(event->edit.text));
            _pg_insobj(dict, "start", PyLong_FromLong(event->edit.start));
            _pg_insobj(dict, "length", PyLong_FromLong(event->edit.length));
            break;
        /*  https://wiki.libsdl.org/SDL_DropEvent */
        case SDL_DROPFILE:
#if SDL_VERSION_ATLEAST(3, 0, 0)
            _pg_insobj(dict, "file", PyUnicode_FromString(event->drop.data));
            /* No need to free event->drop.data, SDL3 handles it */
#else
            _pg_insobj(dict, "file", PyUnicode_FromString(event->drop.file));
            SDL_free(event->drop.file);
#endif
            break;
        case SDL_DROPTEXT:
#if SDL_VERSION_ATLEAST(3, 0, 0)
            _pg_insobj(dict, "text", PyUnicode_FromString(event->drop.data));
            /* No need to free event->drop.data, SDL3 handles it */
#else
            _pg_insobj(dict, "text", PyUnicode_FromString(event->drop.file));
            SDL_free(event->drop.file);
#endif
            break;
        case SDL_DROPBEGIN:
        case SDL_DROPCOMPLETE:
            break;
        case SDL_CONTROLLERAXISMOTION:
            /* https://wiki.libsdl.org/SDL_ControllerAxisEvent */
#if SDL_VERSION_ATLEAST(3, 0, 0)
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->gaxis.which));
            _pg_insobj(dict, "axis", PyLong_FromLong(event->gaxis.axis));
            _pg_insobj(dict, "value", PyLong_FromLong(event->gaxis.value));
#else
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->caxis.which));
            _pg_insobj(dict, "axis", PyLong_FromLong(event->caxis.axis));
            _pg_insobj(dict, "value", PyLong_FromLong(event->caxis.value));
#endif
            break;
        case SDL_CONTROLLERBUTTONDOWN:
        case SDL_CONTROLLERBUTTONUP:
#if SDL_VERSION_ATLEAST(3, 0, 0)
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->gbutton.which));
            _pg_insobj(dict, "button", PyLong_FromLong(event->gbutton.button));
#else
            /* https://wiki.libsdl.org/SDL_ControllerButtonEvent */
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->cbutton.which));
            _pg_insobj(dict, "button", PyLong_FromLong(event->cbutton.button));
#endif
            break;
        case SDL_CONTROLLERDEVICEADDED:
#if SDL_VERSION_ATLEAST(3, 0, 0)
            _pg_insobj(dict, "device_index",
                       get_joy_device_index(event->gdevice.which));
            _pg_insobj(dict, "guid", get_joy_guid(event->gdevice.which));
#else
            _pg_insobj(dict, "device_index",
                       PyLong_FromLong(event->cdevice.which));
            _pg_insobj(dict, "guid", get_joy_guid(event->jdevice.which));
#endif
            break;
        case SDL_JOYDEVICEADDED:
#if SDL_VERSION_ATLEAST(3, 0, 0)
            _pg_insobj(dict, "device_index",
                       get_joy_device_index(event->jdevice.which));
#else
            _pg_insobj(dict, "device_index",
                       PyLong_FromLong(event->jdevice.which));
#endif
            _pg_insobj(dict, "guid", get_joy_guid(event->jdevice.which));
            break;
        case SDL_CONTROLLERDEVICEREMOVED:
        case SDL_CONTROLLERDEVICEREMAPPED:
            /* https://wiki.libsdl.org/SDL_ControllerDeviceEvent */
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->cdevice.which));
            break;
        case SDL_JOYDEVICEREMOVED:
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->jdevice.which));
            break;
        case SDL_CONTROLLERTOUCHPADDOWN:
        case SDL_CONTROLLERTOUCHPADMOTION:
        case SDL_CONTROLLERTOUCHPADUP:
#if SDL_VERSION_ATLEAST(3, 0, 0)
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->gtouchpad.which));
            _pg_insobj(dict, "touch_id",
                       PyLong_FromLongLong(event->gtouchpad.touchpad));
            _pg_insobj(dict, "finger_id",
                       PyLong_FromLongLong(event->gtouchpad.finger));
            _pg_insobj(dict, "x", PyFloat_FromDouble(event->gtouchpad.x));
            _pg_insobj(dict, "y", PyFloat_FromDouble(event->gtouchpad.y));
            _pg_insobj(dict, "pressure",
                       PyFloat_FromDouble(event->gtouchpad.pressure));
#else
            _pg_insobj(dict, "instance_id",
                       PyLong_FromLong(event->ctouchpad.which));
            _pg_insobj(dict, "touch_id",
                       PyLong_FromLongLong(event->ctouchpad.touchpad));
            _pg_insobj(dict, "finger_id",
                       PyLong_FromLongLong(event->ctouchpad.finger));
            _pg_insobj(dict, "x", PyFloat_FromDouble(event->ctouchpad.x));
            _pg_insobj(dict, "y", PyFloat_FromDouble(event->ctouchpad.y));
            _pg_insobj(dict, "pressure",
                       PyFloat_FromDouble(event->ctouchpad.pressure));
#endif
            break;

#if !SDL_VERSION_ATLEAST(3, 0, 0)
#ifdef WIN32
        case SDL_SYSWMEVENT:
            _pg_insobj(dict, "hwnd",
                       PyLong_FromLongLong(
                           (long long)(event->syswm.msg->msg.win.hwnd)));
            _pg_insobj(dict, "msg",
                       PyLong_FromLong(event->syswm.msg->msg.win.msg));
            _pg_insobj(dict, "wparam",
                       PyLong_FromLongLong(event->syswm.msg->msg.win.wParam));
            _pg_insobj(dict, "lparam",
                       PyLong_FromLongLong(event->syswm.msg->msg.win.lParam));
            break;
#endif /* WIN32 */

#if (defined(unix) || defined(__unix__) || defined(_AIX) ||     \
     defined(__OpenBSD__)) &&                                   \
    (defined(SDL_VIDEO_DRIVER_X11) && !defined(__CYGWIN32__) && \
     !defined(ENABLE_NANOX) && !defined(__QNXNTO__))
        case SDL_SYSWMEVENT:
            if (event->syswm.msg->subsystem == SDL_SYSWM_X11) {
                XEvent *xevent = (XEvent *)&event->syswm.msg->msg.x11.event;
                obj =
                    PyBytes_FromStringAndSize((char *)xevent, sizeof(XEvent));
                _pg_insobj(dict, "event", obj);
            }
            break;
#endif /* (defined(unix) || ... */
#endif /* !SDL_VERSION_ATLEAST(3, 0, 0) */
    } /* switch (event->type) */
    /* Events that don't have any attributes are not handled in switch
     * statement */
    SDL_Window *window;
    switch (event->type) {
        case PGE_WINDOWSHOWN:
        case PGE_WINDOWHIDDEN:
        case PGE_WINDOWEXPOSED:
        case PGE_WINDOWMOVED:
        case PGE_WINDOWRESIZED:
        case PGE_WINDOWSIZECHANGED:
        case PGE_WINDOWMINIMIZED:
        case PGE_WINDOWMAXIMIZED:
        case PGE_WINDOWRESTORED:
        case PGE_WINDOWENTER:
        case PGE_WINDOWLEAVE:
        case PGE_WINDOWFOCUSGAINED:
        case PGE_WINDOWFOCUSLOST:
        case PGE_WINDOWCLOSE:
        case PGE_WINDOWTAKEFOCUS:
        case PGE_WINDOWHITTEST:
        case PGE_WINDOWICCPROFCHANGED:
        case PGE_WINDOWDISPLAYCHANGED: {
            window = SDL_GetWindowFromID(event->window.windowID);
            break;
        }
        case SDL_TEXTEDITING: {
            window = SDL_GetWindowFromID(event->edit.windowID);
            break;
        }
        case SDL_TEXTINPUT: {
            window = SDL_GetWindowFromID(event->text.windowID);
            break;
        }
        case SDL_DROPBEGIN:
        case SDL_DROPCOMPLETE:
        case SDL_DROPTEXT:
        case SDL_DROPFILE: {
            window = SDL_GetWindowFromID(event->drop.windowID);
            break;
        }
        case SDL_KEYDOWN:
        case SDL_KEYUP: {
            window = SDL_GetWindowFromID(event->key.windowID);
            break;
        }
        case SDL_MOUSEWHEEL: {
            window = SDL_GetWindowFromID(event->wheel.windowID);
            break;
        }
        case SDL_MOUSEMOTION: {
            window = SDL_GetWindowFromID(event->motion.windowID);
            break;
        }
        case SDL_MOUSEBUTTONDOWN:
        case SDL_MOUSEBUTTONUP: {
            window = SDL_GetWindowFromID(event->button.windowID);
            break;
        }
        case SDL_FINGERMOTION:
        case SDL_FINGERDOWN:
        case SDL_FINGERUP: {
            window = SDL_GetWindowFromID(event->tfinger.windowID);
            break;
        }
        default: {
            return dict;
        }
    }
    PyObject *pgWindow;
#if SDL_VERSION_ATLEAST(3, 0, 0)
    if (!window || !(pgWindow = SDL_GetPointerProperty(
                         SDL_GetWindowProperties(window), "pg_window", NULL)))
#else
    if (!window || !(pgWindow = SDL_GetWindowData(window, "pg_window")))
#endif
    {
        pgWindow = Py_None;
    }
    Py_INCREF(pgWindow);
    _pg_insobj(dict, "window", pgWindow);
    return dict;
}

static PyObject *
pgEvent_GetType(void)
{
    if (!_event_class)
        return RAISE(PyExc_RuntimeError, "event type is currently unknown");

    Py_INCREF(_event_class);
    return _event_class;
}

static PyObject *
pgEvent_FromTypeAndDict(int e_type, PyObject *dict)
{
    PyObject *ret = NULL;
    PyObject *args = NULL;

    PyObject *e_typeo = pgEvent_GetType();
    if (!e_typeo)
        return NULL;

    PyObject *num = PyLong_FromLong(e_type);
    if (!num)
        goto finalize;

    args = PyTuple_New(1);

    if (!args) {
        Py_DECREF(num);
        goto finalize;
    }

    PyTuple_SetItem(args, 0, num);

    ret = PyObject_Call(e_typeo, args, dict);

finalize:
    Py_DECREF(e_typeo);
    Py_XDECREF(args);
    return ret;
}

static int
pgEvent_GetEventType(PyObject *event)
{
    PyObject *e_typeo = PyObject_GetAttrString(event, "type");

    if (!e_typeo) {
        return -1;
    }

    long e_type = PyLong_AsLong(e_typeo);
    Py_DECREF(e_typeo);

    if (PyErr_Occurred()) {
        return -1;
    }

    if (e_type < 0 || e_type >= PG_NUMEVENTS) {
        RAISERETURN(PyExc_ValueError, "event type out of range", -1)
    }

    return e_type;
}

static PyObject *
pgEvent_New(SDL_Event *event)
{
    Uint32 e_type;
    PyObject *obj_or_dict = NULL;

    if (event) {
        e_type = _pg_pgevent_deproxify(event->type);
        obj_or_dict = dict_or_obj_from_event(event);
    }
    else {
        e_type = SDL_NOEVENT;
    }

    if (!obj_or_dict ||
        PyObject_IsInstance(obj_or_dict, (PyObject *)&PyDict_Type)) {
        if (PyErr_Occurred())
            return NULL;

        PyObject *ret = pgEvent_FromTypeAndDict(e_type, obj_or_dict);
        Py_XDECREF(obj_or_dict);
        return ret;
    }

    return obj_or_dict;
}

static int
pgEvent_Check(PyObject *obj)
{
    PyObject *e_type = pgEvent_GetType();
    if (!e_type)
        return -1;
    int res = PyObject_IsInstance(obj, e_type);
    Py_DECREF(e_type);
    return res;
}

/* event module functions */

static PyObject *
set_grab(PyObject *self, PyObject *arg)
{
    int doit = PyObject_IsTrue(arg);
    if (doit == -1)
        return NULL;

    VIDEO_INIT_CHECK();

    SDL_Window *win = pg_GetDefaultWindow();
    if (win) {
        if (doit) {
#if SDL_VERSION_ATLEAST(3, 0, 0)
            SDL_SetWindowMouseGrab(win, true);
            SDL_SetWindowRelativeMouseMode(win, !PG_CursorVisible());
#else
            SDL_SetWindowGrab(win, SDL_TRUE);
            if (PG_CursorVisible() == SDL_DISABLE)
                SDL_SetRelativeMouseMode(1);
            else
                SDL_SetRelativeMouseMode(0);
#endif
        }
        else {
#if SDL_VERSION_ATLEAST(3, 0, 0)
            SDL_SetWindowMouseGrab(win, false);
            SDL_SetWindowRelativeMouseMode(win, false);
#else
            SDL_SetWindowGrab(win, SDL_FALSE);
            SDL_SetRelativeMouseMode(0);
#endif
        }
    }

    Py_RETURN_NONE;
}

static PyObject *
get_grab(PyObject *self, PyObject *_null)
{
    SDL_Window *win;
    SDL_bool mode = SDL_FALSE;

    VIDEO_INIT_CHECK();
    win = pg_GetDefaultWindow();
    if (win) {
#if SDL_VERSION_ATLEAST(3, 0, 0)
        mode = SDL_GetWindowMouseGrab(win);
#else
        mode = SDL_GetWindowGrab(win);
#endif
    }
    return PyBool_FromLong(mode);
}

static void
_pg_event_pump(int dopump)
{
    if (dopump) {
        /* This needs to be reset just before calling pump, e.g. on calls to
         * pygame.event.get(), but not on pygame.event.get(pump=False). */
        memset(input_buffer, 0, sizeof(input_buffer));

        SDL_PumpEvents();
    }

    /* WINDOWEVENT translation needed only on SDL2 */
#if !SDL_VERSION_ATLEAST(3, 0, 0)
    /* We need to translate WINDOWEVENTS. But if we do that from the
     * from event filter, internal SDL stuff that rely on WINDOWEVENT
     * might break. So after every event pump, we translate events from
     * here */
    SDL_FilterEvents(_pg_translate_windowevent, NULL);
#endif
}

static int
_pg_event_wait(SDL_Event *event, int timeout)
{
    /* Custom re-implementation of SDL_WaitEventTimeout, doing this has
     * many advantages. This is copied from SDL source code, with a few
     * minor modifications */
    Uint64 finish = 0;

    if (timeout > 0)
        finish = PG_GetTicks() + timeout;

    while (1) {
        _pg_event_pump(1); /* Use our custom pump here */
        switch (PG_PEEP_EVENT_ALL(event, 1, SDL_GETEVENT)) {
            case -1:
                return 0; /* Because this never happens, SDL does it too*/
            case 1:
                return 1;

            default:
                if (timeout >= 0 && PG_GetTicks() >= finish) {
                    /* no events */
                    return 0;
                }
                SDL_Delay(1);
        }
    }
}

static PyObject *
pg_event_pump(PyObject *self, PyObject *obj)
{
    VIDEO_INIT_CHECK();
    int dopump = PyObject_IsTrue(obj);

    if (dopump < 0)
        return NULL;

    _pg_event_pump(dopump);
    Py_RETURN_NONE;
}

static PyObject *
pg_event_poll(PyObject *self, PyObject *_null)
{
    SDL_Event event;
    VIDEO_INIT_CHECK();

    /* polling is just waiting for 0 timeout */
    if (!_pg_event_wait(&event, 0))
        return pgEvent_New(NULL);
    return pgEvent_New(&event);
}

static PyObject *
pg_event_wait(PyObject *self, PyObject *args, PyObject *kwargs)
{
    SDL_Event event;
    int status, timeout = 0;
    static char *kwids[] = {"timeout", NULL};

    VIDEO_INIT_CHECK();

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|i", kwids, &timeout)) {
        return NULL;
    }

    if (!timeout)
        timeout = -1;

    Py_BEGIN_ALLOW_THREADS;
    status = _pg_event_wait(&event, timeout);
    Py_END_ALLOW_THREADS;

    if (!status)
        return pgEvent_New(NULL);
    return pgEvent_New(&event);
}

char *
pgEvent_GetKeyDownInfo(void)
{
    return input_buffer + INPUT_BUFFER_PRESSED_OFFSET;
}

char *
pgEvent_GetKeyUpInfo(void)
{
    return input_buffer + INPUT_BUFFER_RELEASED_OFFSET;
}

char *
pgEvent_GetMouseButtonDownInfo(void)
{
    return input_buffer + INPUT_BUFFER_MOUSE_PRESSED_OFFSET;
}

char *
pgEvent_GetMouseButtonUpInfo(void)
{
    return input_buffer + INPUT_BUFFER_MOUSE_RELEASED_OFFSET;
}

static PyObject *
_pg_get_event(PyObject *self, PyObject *obj)
{
    SDL_Event ev;
    int e_type = PyLong_AsLong(obj);

    if (e_type == -1 && PyErr_Occurred())
        return NULL;

    int ret;
    if (e_type == -1)
        ret = PG_PEEP_EVENT_ALL(&ev, 1, SDL_GETEVENT);
    else
        ret = PG_PEEP_EVENT(&ev, 1, SDL_GETEVENT, e_type);
    if (ret == -1)
        return RAISE(pgExc_SDLError, SDL_GetError());
    else if (ret == 0)
        Py_RETURN_NONE;
    return pgEvent_New(&ev);
}

static PyObject *
_pg_peek_event(PyObject *self, PyObject *obj)
{
    SDL_Event ev;
    int e_type = PyLong_AsLong(obj);

    if (e_type == -1 && PyErr_Occurred())
        return NULL;

    int ret;
    if (e_type == -1)
        ret = PG_PEEP_EVENT_ALL(&ev, 1, SDL_PEEKEVENT);
    else
        ret = PG_PEEP_EVENT(&ev, 1, SDL_PEEKEVENT, e_type);
    if (ret == -1)
        return RAISE(pgExc_SDLError, SDL_GetError());
    return PyBool_FromLong(ret);
}

static PyObject *
_pg_video_check(PyObject *self, PyObject *_null)
{
    VIDEO_INIT_CHECK();
    Py_RETURN_NONE;
}

static PyObject *
_pg_proxify_event_type(PyObject *self, PyObject *obj)
{
    int e_type = PyLong_AsLong(obj);

    if (e_type == -1 && PyErr_Occurred())
        return NULL;

    return PyLong_FromLong(_pg_pgevent_proxify((Uint32)e_type));
}

/* You might notice how we do event blocking stuff on proxy events and
 * not the real SDL events. We do this because we want SDL events to pass
 * through our event filter, to do emulation stuff correctly. Then the
 * event is filtered after that */

static PyObject *
pg_event_post(PyObject *self, PyObject *obj)
{
    VIDEO_INIT_CHECK();
    int is_event = pgEvent_Check(obj);
    if (is_event < 0)
        return NULL;
    else if (!is_event)
        return RAISE(PyExc_TypeError, "argument must be an Event object");

    int e_type = pgEvent_GetEventType(obj);

    if (PyErr_Occurred())
        return NULL;

    int res = pg_post_event(e_type, obj);

    switch (res) {
        case 0:
            Py_RETURN_FALSE;
        case 1:
            Py_RETURN_TRUE;
        default:
            return RAISE(pgExc_SDLError, SDL_GetError());
    }
}

static PyObject *
pg_event_allowed_set(PyObject *self, PyObject *args)
{
    VIDEO_INIT_CHECK();

    int e_type, e_flag;
    PyObject *e_flago = NULL;

    if (!PyArg_ParseTuple(args, "iO", &e_type, &e_flago))
        return NULL;

    if (e_type < 0 || e_type >= PG_NUMEVENTS) {
        PyErr_SetString(PyExc_ValueError, "event type out of range");
        return NULL;
    }

    e_flag = PyObject_IsTrue(e_flago);

    if (e_flag < 0)
        return NULL;

    PG_SetEventEnabled(_pg_pgevent_proxify(e_type),
                       e_flag ? SDL_TRUE : SDL_FALSE);

    // Never block events that are needed for proecesing.
    if (e_type == PGE_KEYREPEAT)
        PG_SetEventEnabled(e_type, SDL_TRUE);
#if !SDL_VERSION_ATLEAST(3, 0, 0)
    else if (e_type == SDL_WINDOWEVENT)
        PG_SetEventEnabled(e_type, SDL_TRUE);
#endif
    else
        PG_SetEventEnabled(e_type, e_flag ? SDL_TRUE : SDL_FALSE);

    Py_RETURN_NONE;
}

static PyObject *
pg_event_allowed_get(PyObject *self, PyObject *obj)
{
    VIDEO_INIT_CHECK();

    int e_type = PyLong_AsLong(obj);

    if (PyErr_Occurred())
        return NULL;

    else if (e_type < 0 || e_type >= PG_NUMEVENTS) {
        PyErr_SetString(PyExc_ValueError, "event type out of range");
        return NULL;
    }

    if (PG_EventEnabled(e_type) == SDL_TRUE)
        Py_RETURN_TRUE;
    Py_RETURN_FALSE;
}

static PyObject *
pg_event_register_event_class(PyObject *self, PyObject *obj)
{
    if (!(PyType_Check(obj) && PyCallable_Check(obj)))
        return RAISE(PyExc_ValueError, "expected a type");

    Py_INCREF(obj);
    Py_XDECREF(_event_class);
    _event_class = obj;
    Py_RETURN_NONE;
}

void
pg_event_free(PyObject *self)
{
    Py_XDECREF(_event_class);
    _event_class = NULL;
}

static PyMethodDef _event_methods[] = {
    {"_internal_mod_init", (PyCFunction)pgEvent_AutoInit, METH_NOARGS,
     "auto initialize for event module"},
    {"_internal_mod_quit", (PyCFunction)pgEvent_AutoQuit, METH_NOARGS,
     "auto quit for event module"},

    {"set_grab", set_grab, METH_O, DOC_EVENT_SETGRAB},
    {"get_grab", (PyCFunction)get_grab, METH_NOARGS, DOC_EVENT_GETGRAB},

    {"pump", (PyCFunction)pg_event_pump, METH_O, DOC_EVENT_PUMP},
    {"wait", (PyCFunction)pg_event_wait, METH_VARARGS | METH_KEYWORDS,
     DOC_EVENT_WAIT},
    {"poll", (PyCFunction)pg_event_poll, METH_NOARGS, DOC_EVENT_POLL},
    {"post", (PyCFunction)pg_event_post, METH_O, DOC_EVENT_POST},

    {"allowed_get", (PyCFunction)pg_event_allowed_get, METH_O},
    {"allowed_set", (PyCFunction)pg_event_allowed_set, METH_VARARGS},
    {"register_event_class", (PyCFunction)pg_event_register_event_class,
     METH_O},
    {"video_check", (PyCFunction)_pg_video_check, METH_NOARGS},
    {"_get", (PyCFunction)_pg_get_event, METH_O},
    {"_peek", (PyCFunction)_pg_peek_event, METH_O},
    {"_proxify_event_type", (PyCFunction)_pg_proxify_event_type, METH_O},

    {NULL, NULL, 0, NULL}};

MODINIT_DEFINE(_event)
{
    PyObject *module, *apiobj;
    static void *c_api[PYGAMEAPI_EVENT_NUMSLOTS];

    static struct PyModuleDef _module = {
        PyModuleDef_HEAD_INIT,  "event", DOC_EVENT, -1,
        _event_methods,         NULL,    NULL,      NULL,
        (freefunc)pg_event_free};

    /* imported needed apis; Do this first so if there is an error
       the module is not loaded.
    */
    import_pygame_base();
    if (PyErr_Occurred()) {
        return NULL;
    }

    import_pygame_joystick();
    if (PyErr_Occurred()) {
        return NULL;
    }

    /* create the module */
    module = PyModule_Create(&_module);
    if (!module) {
        return NULL;
    }

    /* export the c api */
    assert(PYGAMEAPI_EVENT_NUMSLOTS == 13);
    c_api[0] = pgEvent_GetType;
    c_api[1] = pgEvent_New;
    c_api[2] = pg_post_event;
    c_api[3] = pg_post_event_steal;
    c_api[4] = pg_EnableKeyRepeat;
    c_api[5] = pg_GetKeyRepeat;
    c_api[6] = pgEvent_GetKeyDownInfo;
    c_api[7] = pgEvent_GetKeyUpInfo;
    c_api[8] = pgEvent_GetMouseButtonDownInfo;
    c_api[9] = pgEvent_GetMouseButtonUpInfo;
    c_api[10] = pgEvent_Check;
    c_api[11] = pgEvent_FromTypeAndDict;
    c_api[12] = pgEvent_GetEventType;

    apiobj = encapsulate_api(c_api, "_event");
    if (PyModule_AddObject(module, PYGAMEAPI_LOCAL_ENTRY, apiobj)) {
        Py_XDECREF(apiobj);
        Py_DECREF(module);
        return NULL;
    }

    SDL_RegisterEvents(PG_NUMEVENTS - SDL_USEREVENT);
    return module;
}
