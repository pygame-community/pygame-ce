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

/* This will use PYGAMEAPI_EXTERN_SLOTS instead
 * of PYGAMEAPI_DEFINE_SLOTS for base modules.
 */
#ifndef _PYGAME_INTERNAL_H
#define _PYGAME_INTERNAL_H

#include "pgplatform.h"
/*
    If PY_SSIZE_T_CLEAN is defined before including Python.h, length is a
    Py_ssize_t rather than an int for all # variants of formats (s#, y#, etc.)
*/
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "include/pythoncapi_compat.h"

/* Ensure PyPy-specific code is not in use when running on GraalPython (PR
 * #2580) */
#if defined(GRAALVM_PYTHON) && defined(PYPY_VERSION)
#undef PYPY_VERSION
#endif

#ifdef PG_SDL3
#include <SDL3/SDL.h>
#else
#include <SDL.h>
#endif

#include "stdbool.h"

#if SDL_VERSION_ATLEAST(3, 0, 0)
#define PG_ShowCursor SDL_ShowCursor
#define PG_HideCursor SDL_HideCursor
#define PG_CursorVisible SDL_CursorVisible

#define PG_INIT_NOPARACHUTE 0

// UINT16 audio no longer exists in SDL3
#define PG_AUDIO_U16LSB 0
#define PG_AUDIO_U16MSB 0
#define PG_AUDIO_U16SYS 0
#define PG_AUDIO_U16 0

// Allowed changes no longer exists, your request gets emulated if unavailable
#define PG_AUDIO_ALLOW_FREQUENCY_CHANGE 0
#define PG_AUDIO_ALLOW_FORMAT_CHANGE 0
#define PG_AUDIO_ALLOW_CHANNELS_CHANGE 0
#define PG_AUDIO_ALLOW_ANY_CHANGE 0

// Todo: deal with multigesture.. See
// https://github.com/pygame-community/pygame-ce/issues/2420
#define PG_MULTIGESTURE 0

#define PG_JOYBALLMOTION 0

#define PG_CreateSurface SDL_CreateSurface
#define PG_CreateSurfaceFrom SDL_CreateSurfaceFrom
#define PG_ConvertSurface SDL_ConvertSurface
#define PG_ConvertSurfaceFormat SDL_ConvertSurface

#define PG_PixelFormatEnum SDL_PixelFormat

#define PG_SurfaceHasRLE SDL_SurfaceHasRLE

#define PG_SoftStretchNearest(src, srcrect, dst, dstrect) \
    SDL_SoftStretch(src, srcrect, dst, dstrect, SDL_SCALEMODE_NEAREST)

/* Emulating SDL2 SDL_LockMutex API. In SDL3, it returns void. */
static inline int
PG_LockMutex(SDL_mutex *mutex)
{
    SDL_LockMutex(mutex);
    return 0;
}

/* Emulating SDL2 SDL_UnlockMutex API. In SDL3, it returns void. */
static inline int
PG_UnlockMutex(SDL_mutex *mutex)
{
    SDL_UnlockMutex(mutex);
    return 0;
}

#define PG_SURF_BitsPerPixel(surf) SDL_BITSPERPIXEL(surf->format)
#define PG_SURF_BytesPerPixel(surf) SDL_BYTESPERPIXEL(surf->format)
#define PG_FORMAT_BitsPerPixel(format) format->bits_per_pixel
#define PG_FORMAT_BytesPerPixel(format) format->bytes_per_pixel
#define PG_SURF_FORMATENUM(surf) surf->format

#define PG_FORMAT_R_LOSS(format) (8 - format->Rbits)
#define PG_FORMAT_G_LOSS(format) (8 - format->Gbits)
#define PG_FORMAT_B_LOSS(format) (8 - format->Bbits)
#define PG_FORMAT_A_LOSS(format) (8 - format->Abits)

#define PG_PixelFormat const SDL_PixelFormatDetails

static inline bool
PG_GetSurfaceDetails(SDL_Surface *surf, PG_PixelFormat **format_p,
                     SDL_Palette **palette_p)
{
    *palette_p = SDL_GetSurfacePalette(surf);
    *format_p = SDL_GetPixelFormatDetails(surf->format);
    return *format_p != NULL;
}

static inline PG_PixelFormat *
PG_GetSurfaceFormat(SDL_Surface *surf)
{
    return SDL_GetPixelFormatDetails(surf->format);
}

#define PG_GetSurfacePalette SDL_GetSurfacePalette

#define PG_GetRGBA SDL_GetRGBA
#define PG_GetRGB SDL_GetRGB
#define PG_MapRGBA SDL_MapRGBA
#define PG_MapRGB SDL_MapRGB

/* Mask to test if surface flags are in a fullscreen window. */
#define PG_WINDOW_FULLSCREEN_INCLUSIVE SDL_WINDOW_FULLSCREEN

#define PG_SetEventEnabled(type, enabled) SDL_SetEventEnabled(type, enabled)
#define PG_EventEnabled(type) SDL_EventEnabled(type)
#define PG_SetJoystickEventsEnabled(enabled) \
    SDL_SetJoystickEventsEnabled(enabled)

#define PG_FIND_VNUM_MAJOR(ver) SDL_VERSIONNUM_MAJOR(ver)
#define PG_FIND_VNUM_MINOR(ver) SDL_VERSIONNUM_MINOR(ver)
#define PG_FIND_VNUM_MICRO(ver) SDL_VERSIONNUM_MICRO(ver)

#define PG_INIT_TIMER 0

#define PG_GetSurfaceClipRect SDL_GetSurfaceClipRect

#else /* ~SDL_VERSION_ATLEAST(3, 0, 0)*/
#define PG_ShowCursor() SDL_ShowCursor(SDL_ENABLE)
#define PG_HideCursor() SDL_ShowCursor(SDL_DISABLE)
#define PG_CursorVisible() SDL_ShowCursor(SDL_QUERY)

#define PG_INIT_NOPARACHUTE SDL_INIT_NOPARACHUTE

#define PG_AUDIO_U16LSB AUDIO_U16LSB
#define PG_AUDIO_U16MSB AUDIO_U16MSB
#define PG_AUDIO_U16SYS AUDIO_U16SYS
#define PG_AUDIO_U16 AUDIO_U16

#define PG_AUDIO_ALLOW_FREQUENCY_CHANGE SDL_AUDIO_ALLOW_FREQUENCY_CHANGE
#define PG_AUDIO_ALLOW_FORMAT_CHANGE SDL_AUDIO_ALLOW_FORMAT_CHANGE
#define PG_AUDIO_ALLOW_CHANNELS_CHANGE SDL_AUDIO_ALLOW_CHANNELS_CHANGE
#define PG_AUDIO_ALLOW_ANY_CHANGE SDL_AUDIO_ALLOW_ANY_CHANGE

#define PG_MULTIGESTURE SDL_MULTIGESTURE

#define PG_JOYBALLMOTION SDL_JOYBALLMOTION

#define PG_CreateSurface(width, height, format) \
    SDL_CreateRGBSurfaceWithFormat(0, width, height, 0, format)
#define PG_CreateSurfaceFrom(width, height, format, pixels, pitch) \
    SDL_CreateRGBSurfaceWithFormatFrom(pixels, width, height, 0, pitch, format)
#define PG_ConvertSurface(src, fmt) SDL_ConvertSurface(src, fmt, 0)
#define PG_ConvertSurfaceFormat(src, pixel_format) \
    SDL_ConvertSurfaceFormat(src, pixel_format, 0)

#define PG_PixelFormatEnum SDL_PixelFormatEnum

#define PG_SoftStretchNearest(src, srcrect, dst, dstrect) \
    SDL_SoftStretch(src, srcrect, dst, dstrect)

static inline int
PG_LockMutex(SDL_mutex *mutex)
{
    return SDL_LockMutex(mutex);
}

static inline int
PG_UnlockMutex(SDL_mutex *mutex)
{
    return SDL_UnlockMutex(mutex);
}

#define PG_SURF_BitsPerPixel(surf) surf->format->BitsPerPixel
#define PG_SURF_BytesPerPixel(surf) surf->format->BytesPerPixel
#define PG_FORMAT_BitsPerPixel(format) format->BitsPerPixel
#define PG_FORMAT_BytesPerPixel(format) format->BytesPerPixel
#define PG_SURF_FORMATENUM(surf) surf->format->format

#define PG_FORMAT_R_LOSS(format) format->Rloss
#define PG_FORMAT_G_LOSS(format) format->Gloss
#define PG_FORMAT_B_LOSS(format) format->Bloss
#define PG_FORMAT_A_LOSS(format) format->Aloss

#define PG_PixelFormat SDL_PixelFormat

static inline bool
PG_GetSurfaceDetails(SDL_Surface *surf, PG_PixelFormat **format_p,
                     SDL_Palette **palette_p)
{
    *format_p = surf->format;
    *palette_p = surf->format->palette;
    return true;
}

static inline PG_PixelFormat *
PG_GetSurfaceFormat(SDL_Surface *surf)
{
    return surf->format;
}

static inline SDL_Palette *
PG_GetSurfacePalette(SDL_Surface *surf)
{
    return surf->format->palette;
}

// NOTE:
// palette is part of the format in SDL2, so these functions below have it
// as a separate parameter to be consistent with the SDL3 signature.
// They are ignoring the palette parameter, but not the palette data.

static inline void
PG_GetRGBA(Uint32 pixel, PG_PixelFormat *format, const SDL_Palette *palette,
           Uint8 *r, Uint8 *g, Uint8 *b, Uint8 *a)
{
    SDL_GetRGBA(pixel, format, r, g, b, a);
}

static inline void
PG_GetRGB(Uint32 pixel, PG_PixelFormat *format, const SDL_Palette *palette,
          Uint8 *r, Uint8 *g, Uint8 *b)
{
    SDL_GetRGB(pixel, format, r, g, b);
}

static inline Uint32
PG_MapRGBA(PG_PixelFormat *format, const SDL_Palette *palette, Uint8 r,
           Uint8 g, Uint8 b, Uint8 a)
{
    return SDL_MapRGBA(format, r, g, b, a);
}

static inline Uint32
PG_MapRGB(PG_PixelFormat *format, const SDL_Palette *palette, Uint8 r, Uint8 g,
          Uint8 b)
{
    return SDL_MapRGB(format, r, g, b);
}

/* Mask to test if surface flags are in a fullscreen window.
 * SDL_WINDOW_FULLSCREEN_DESKTOP works here because it also contains
 * SDL_WINDOW_FULLSCREEN. */
#define PG_WINDOW_FULLSCREEN_INCLUSIVE SDL_WINDOW_FULLSCREEN_DESKTOP

/* SDL_EventState is meant to take SDL_IGNORE or SDL_ENABLE, but it also
 * works identically with SDL_FALSE and SDL_TRUE, because they evaluate to
 * the same values, respectively. */
#define PG_SetEventEnabled(type, enabled) SDL_EventState(type, enabled)
#define PG_EventEnabled(type) SDL_EventState(type, SDL_QUERY)
#define PG_SetJoystickEventsEnabled(enabled) SDL_JoystickEventState(enabled)

#define PG_FIND_VNUM_MAJOR(ver) ver.major
#define PG_FIND_VNUM_MINOR(ver) ver.minor
#define PG_FIND_VNUM_MICRO(ver) ver.patch

#define PG_INIT_TIMER SDL_INIT_TIMER

#define PG_SurfaceHasRLE SDL_HasSurfaceRLE

static inline bool
PG_GetSurfaceClipRect(SDL_Surface *surface, SDL_Rect *rect)
{
    *rect = surface->clip_rect;
    return true;
}
#endif

/* DictProxy is useful for event posting with an arbitrary dict. Maintains
 * state of number of events on queue and whether the owner of this struct
 * wants this dict freed. This DictProxy is only to be freed when there are no
 * more instances of this DictProxy on the event queue. Access to this is
 * safeguarded with a per-proxy spinlock, which is more optimal than having
 * to hold GIL in case of event timers */
typedef struct _pgEventDictProxy {
    PyObject *dict;
    SDL_SpinLock lock;
    int num_on_queue;
    Uint8 do_free_at_end;
} pgEventDictProxy;

/* SDL 1.2 constants removed from SDL 2 */
typedef enum {
    SDL_HWSURFACE = 0,
    SDL_RESIZABLE = SDL_WINDOW_RESIZABLE,
    SDL_ASYNCBLIT = 0,
    SDL_OPENGL = SDL_WINDOW_OPENGL,
    SDL_OPENGLBLIT = 0,
    SDL_ANYFORMAT = 0,
    SDL_HWPALETTE = 0,
    SDL_DOUBLEBUF = 0,
    SDL_FULLSCREEN = SDL_WINDOW_FULLSCREEN,
    SDL_HWACCEL = 0,
    SDL_SRCCOLORKEY = 0,
    SDL_RLEACCELOK = 0,
    SDL_SRCALPHA = 0,
    SDL_NOFRAME = SDL_WINDOW_BORDERLESS,
    SDL_GL_SWAP_CONTROL = 0,
    TIMER_RESOLUTION = 0
} PygameVideoFlags;

/* the wheel button constants were removed from SDL 2 */
typedef enum {
    PGM_BUTTON_LEFT = SDL_BUTTON_LEFT,
    PGM_BUTTON_RIGHT = SDL_BUTTON_RIGHT,
    PGM_BUTTON_MIDDLE = SDL_BUTTON_MIDDLE,
    PGM_BUTTON_WHEELUP = 4,
    PGM_BUTTON_WHEELDOWN = 5,
    PGM_BUTTON_X1 = SDL_BUTTON_X1 + 2,
    PGM_BUTTON_X2 = SDL_BUTTON_X2 + 2,
    PGM_BUTTON_KEEP = 0x80
} PygameMouseFlags;

typedef enum {
    /* Any SDL_* events here are for backward compatibility. */
    SDL_NOEVENT = 0,

    SDL_ACTIVEEVENT = SDL_USEREVENT,
    SDL_VIDEORESIZE,
    SDL_VIDEOEXPOSE,
#if SDL_VERSION_ATLEAST(3, 0, 0)
    /* SDL_SYSWMEVENT removed in SDL3, define it here for compat */
    SDL_SYSWMEVENT,
#endif

    PGE_MIDIIN,
    PGE_MIDIOUT,
    PGE_KEYREPEAT, /* Special internal pygame event, for managing key-presses
                    */

    /* DO NOT CHANGE THE ORDER OF EVENTS HERE */
    PGE_WINDOWSHOWN,
    PGE_WINDOWHIDDEN,
    PGE_WINDOWEXPOSED,
    PGE_WINDOWMOVED,
    PGE_WINDOWRESIZED,
    PGE_WINDOWSIZECHANGED,
    PGE_WINDOWMINIMIZED,
    PGE_WINDOWMAXIMIZED,
    PGE_WINDOWRESTORED,
    PGE_WINDOWENTER,
    PGE_WINDOWLEAVE,
    PGE_WINDOWFOCUSGAINED,
    PGE_WINDOWFOCUSLOST,
    PGE_WINDOWCLOSE,
    PGE_WINDOWTAKEFOCUS,
    PGE_WINDOWHITTEST,
    PGE_WINDOWICCPROFCHANGED,
    PGE_WINDOWDISPLAYCHANGED,

    /* Here we define PGPOST_* events, events that act as a one-to-one
     * proxy for SDL events (and some extra events too!), the proxy is used
     * internally when pygame users use event.post()
     *
     * At a first glance, these may look redundant, but they are really
     * important, especially with event blocking. If proxy events are
     * not there, blocked events don't make it to our event filter, and
     * that can break a lot of stuff.
     *
     * IMPORTANT NOTE: Do not post events directly with these proxy types,
     * use the appropriate functions from event.c, that handle these proxy
     * events for you.
     * Proxy events are for internal use only */
    PGPOST_EVENTBEGIN, /* mark start of proxy-events */
    PGPOST_ACTIVEEVENT = PGPOST_EVENTBEGIN,
    PGPOST_APP_TERMINATING,
    PGPOST_APP_LOWMEMORY,
    PGPOST_APP_WILLENTERBACKGROUND,
    PGPOST_APP_DIDENTERBACKGROUND,
    PGPOST_APP_WILLENTERFOREGROUND,
    PGPOST_APP_DIDENTERFOREGROUND,
    PGPOST_AUDIODEVICEADDED,
    PGPOST_AUDIODEVICEREMOVED,
    PGPOST_CLIPBOARDUPDATE,
    PGPOST_CONTROLLERAXISMOTION,
    PGPOST_CONTROLLERBUTTONDOWN,
    PGPOST_CONTROLLERBUTTONUP,
    PGPOST_CONTROLLERDEVICEADDED,
    PGPOST_CONTROLLERDEVICEREMOVED,
    PGPOST_CONTROLLERDEVICEREMAPPED,
    PGPOST_CONTROLLERTOUCHPADDOWN,
    PGPOST_CONTROLLERTOUCHPADMOTION,
    PGPOST_CONTROLLERTOUCHPADUP,
    PGPOST_CONTROLLERSENSORUPDATE,
#if !SDL_VERSION_ATLEAST(3, 0, 0)
    PGPOST_DOLLARGESTURE,
    PGPOST_DOLLARRECORD,
#endif
    PGPOST_DROPFILE,
    PGPOST_DROPTEXT,
    PGPOST_DROPBEGIN,
    PGPOST_DROPCOMPLETE,
    PGPOST_FINGERMOTION,
    PGPOST_FINGERDOWN,
    PGPOST_FINGERUP,
    PGPOST_KEYDOWN,
    PGPOST_KEYMAPCHANGED,
    PGPOST_KEYUP,
    PGPOST_JOYAXISMOTION,
    PGPOST_JOYBALLMOTION,
    PGPOST_JOYHATMOTION,
    PGPOST_JOYBUTTONDOWN,
    PGPOST_JOYBUTTONUP,
    PGPOST_JOYDEVICEADDED,
    PGPOST_JOYDEVICEREMOVED,
    PGPOST_LOCALECHANGED,
    PGPOST_MIDIIN,
    PGPOST_MIDIOUT,
    PGPOST_MOUSEMOTION,
    PGPOST_MOUSEBUTTONDOWN,
    PGPOST_MOUSEBUTTONUP,
    PGPOST_MOUSEWHEEL,
#if !SDL_VERSION_ATLEAST(3, 0, 0)
    PGPOST_MULTIGESTURE,
#endif
    PGPOST_NOEVENT,
    PGPOST_QUIT,
    PGPOST_RENDER_TARGETS_RESET,
    PGPOST_RENDER_DEVICE_RESET,
    PGPOST_SYSWMEVENT,
    PGPOST_TEXTEDITING,
    PGPOST_TEXTINPUT,
    PGPOST_VIDEORESIZE,
    PGPOST_VIDEOEXPOSE,
    PGPOST_WINDOWSHOWN,
    PGPOST_WINDOWHIDDEN,
    PGPOST_WINDOWEXPOSED,
    PGPOST_WINDOWMOVED,
    PGPOST_WINDOWRESIZED,
    PGPOST_WINDOWSIZECHANGED,
    PGPOST_WINDOWMINIMIZED,
    PGPOST_WINDOWMAXIMIZED,
    PGPOST_WINDOWRESTORED,
    PGPOST_WINDOWENTER,
    PGPOST_WINDOWLEAVE,
    PGPOST_WINDOWFOCUSGAINED,
    PGPOST_WINDOWFOCUSLOST,
    PGPOST_WINDOWCLOSE,
    PGPOST_WINDOWTAKEFOCUS,
    PGPOST_WINDOWHITTEST,
    PGPOST_WINDOWICCPROFCHANGED,
    PGPOST_WINDOWDISPLAYCHANGED,

    PGE_USEREVENT, /* this event must stay in this position only */

    PG_NUMEVENTS =
        SDL_LASTEVENT /* Not an event. Indicates end of user events. */
} PygameEventCode;

/* SDL1 ACTIVEEVENT state attribute can take the following values */
/* These constant values are directly picked from SDL1 source */
#define SDL_APPMOUSEFOCUS 0x01
#define SDL_APPINPUTFOCUS 0x02
#define SDL_APPACTIVE 0x04

/* Surface flags: based on SDL 1.2 flags */
typedef enum {
    PGS_SWSURFACE = 0x00000000,
    PGS_HWSURFACE = 0x00000001,
    PGS_ASYNCBLIT = 0x00000004,

    PGS_ANYFORMAT = 0x10000000,
    PGS_HWPALETTE = 0x20000000,
    PGS_DOUBLEBUF = 0x40000000,
    PGS_FULLSCREEN = 0x80000000,
    PGS_SCALED = 0x00000200,

    PGS_OPENGL = 0x00000002,
    PGS_OPENGLBLIT = 0x0000000A,
    PGS_RESIZABLE = 0x00000010,
    PGS_NOFRAME = 0x00000020,
    PGS_SHOWN = 0x00000040,  /* Added from SDL 2 */
    PGS_HIDDEN = 0x00000080, /* Added from SDL 2 */

    PGS_HWACCEL = 0x00000100,
    PGS_SRCCOLORKEY = 0x00001000,
    PGS_RLEACCELOK = 0x00002000,
    PGS_RLEACCEL = 0x00004000,
    PGS_SRCALPHA = 0x00010000,
    PGS_PREALLOC = 0x01000000
} PygameSurfaceFlags;

typedef enum {
    PGS_SCROLL_DEFAULT = 0x00000000,
    PGS_SCROLL_REPEAT = 0x00000001,
    PGS_SCROLL_ERASE = 0x00000004
} PygameScrollSurfaceFlags;

#define RAISE(x, y) (PyErr_SetString((x), (y)), NULL)
#define RAISERETURN(x, y, r)   \
    PyErr_SetString((x), (y)); \
    return r;
#define DEL_ATTR_NOT_SUPPORTED_CHECK(name, value)                            \
    do {                                                                     \
        if (!value) {                                                        \
            PyErr_Format(PyExc_AttributeError, "Cannot delete attribute %s", \
                         name);                                              \
            return -1;                                                       \
        }                                                                    \
    } while (0)

#define DEL_ATTR_NOT_SUPPORTED_CHECK_NO_NAME(value)                           \
    do {                                                                      \
        if (!value) {                                                         \
            PyErr_SetString(PyExc_AttributeError, "Cannot delete attribute"); \
            return -1;                                                        \
        }                                                                     \
    } while (0)

/*
 * Initialization checks
 */

#define VIDEO_INIT_CHECK()            \
    if (!SDL_WasInit(SDL_INIT_VIDEO)) \
    return RAISE(pgExc_SDLError, "video system not initialized")

#define JOYSTICK_INIT_CHECK()            \
    if (!SDL_WasInit(SDL_INIT_JOYSTICK)) \
    return RAISE(pgExc_SDLError, "joystick system not initialized")

/* thread check */
#ifdef WITH_THREAD
#define PG_CHECK_THREADS() (1)
#else /* ~WITH_THREAD */
#define PG_CHECK_THREADS() \
    (RAISE(PyExc_NotImplementedError, "Python built without thread support"))
#endif /* ~WITH_THREAD */

/* Update this function if new sequences are added to the fast sequence
 * type. */
#ifndef pgSequenceFast_Check
#define pgSequenceFast_Check(o) (PyList_Check(o) || PyTuple_Check(o))
#endif /* ~pgSequenceFast_Check */

/*
 * event module internals
 */
struct pgEventObject {
    PyObject_HEAD int type;
    PyObject *dict;
};

/*
 * surface module internals
 */
struct pgSubSurface_Data {
    PyObject *owner;
    int offsetx, offsety;
};

/*
 * color module internals
 */
struct pgColorObject {
    PyObject_HEAD Uint8 data[4];
    Uint8 len;
};

typedef enum {
    /* 0b000: Only handle RGB[A] sequence (which includes pygame.Color) */
    PG_COLOR_HANDLE_SIMPLE = 0,

    /* 0b001: In addition to PG_COLOR_HANDLE_SIMPLE, also handle str */
    PG_COLOR_HANDLE_STR = 1,

    /* 0b010: In addition to PG_COLOR_HANDLE_SIMPLE, also handles int */
    PG_COLOR_HANDLE_INT = (PG_COLOR_HANDLE_STR << 1),

    /* 0b100: A specialised flag, used to indicate that only tuple,
       pygame.Color or subtypes of these both are allowed */
    PG_COLOR_HANDLE_RESTRICT_SEQ = (PG_COLOR_HANDLE_INT << 1),

    /* 0b011: equivalent to PG_COLOR_HANDLE_STR | PG_COLOR_HANDLE_INT */
    PG_COLOR_HANDLE_ALL = PG_COLOR_HANDLE_STR | PG_COLOR_HANDLE_INT,
} pgColorHandleFlags;

/*
 * include public API
 */
#include "pgplatform.h"
#include <Python.h>

/* version macros (defined since version 1.9.5) */
#ifndef PG_MAJOR_VERSION
#error PG_MAJOR_VERSION must be defined
#endif

#ifndef PG_MINOR_VERSION
#error PG_MINOR_VERSION must be defined
#endif

#ifndef PG_PATCH_VERSION
#error PG_PATCH_VERSION must be defined
#endif

#ifndef PG_VERSION_TAG
#error PG_VERSION_TAG must be defined
#endif

#define PG_VERSIONNUM(MAJOR, MINOR, PATCH) \
    (1000 * (MAJOR) + 100 * (MINOR) + (PATCH))
#define PG_VERSION_ATLEAST(MAJOR, MINOR, PATCH)                             \
    (PG_VERSIONNUM(PG_MAJOR_VERSION, PG_MINOR_VERSION, PG_PATCH_VERSION) >= \
     PG_VERSIONNUM(MAJOR, MINOR, PATCH))

#include "pgcompat.h"

/* Flag indicating a pg_buffer; used for assertions within callbacks */
#ifndef NDEBUG
#define PyBUF_PYGAME 0x4000
#endif
#define PyBUF_HAS_FLAG(f, F) (((f) & (F)) == (F))

/* Array information exchange struct C type; inherits from Py_buffer
 *
 * Pygame uses its own Py_buffer derived C struct as an internal representation
 * of an imported array buffer. The extended Py_buffer allows for a
 * per-instance release callback,
 */
typedef void (*pybuffer_releaseproc)(Py_buffer *);

typedef struct pg_bufferinfo_s {
    Py_buffer view;
    PyObject *consumer; /* Input: Borrowed reference */
    pybuffer_releaseproc release_buffer;
} pg_buffer;

#include "include/pgimport.h"
#include "pgcompat_rect.h"

/*
 * BASE module
 */
#ifndef PYGAMEAPI_BASE_INTERNAL
#define pgExc_SDLError ((PyObject *)PYGAMEAPI_GET_SLOT(base, 0))

#define pg_RegisterQuit \
    (*(void (*)(void (*)(void)))PYGAMEAPI_GET_SLOT(base, 1))

#define pg_IntFromObj \
    (*(int (*)(PyObject *, int *))PYGAMEAPI_GET_SLOT(base, 2))

#define pg_IntFromObjIndex \
    (*(int (*)(PyObject *, int, int *))PYGAMEAPI_GET_SLOT(base, 3))

#define pg_TwoIntsFromObj \
    (*(int (*)(PyObject *, int *, int *))PYGAMEAPI_GET_SLOT(base, 4))

#define pg_FloatFromObj \
    (*(int (*)(PyObject *, float *))PYGAMEAPI_GET_SLOT(base, 5))

#define pg_FloatFromObjIndex \
    (*(int (*)(PyObject *, int, float *))PYGAMEAPI_GET_SLOT(base, 6))

#define pg_TwoFloatsFromObj \
    (*(int (*)(PyObject *, float *, float *))PYGAMEAPI_GET_SLOT(base, 7))

#define pg_DoubleFromObj \
    (*(int (*)(PyObject *, double *))PYGAMEAPI_GET_SLOT(base, 24))

#define pg_TwoDoublesFromObj \
    (*(int (*)(PyObject *, double *, double *))PYGAMEAPI_GET_SLOT(base, 25))

#define pg_TwoDoublesFromFastcallArgs                   \
    (*(int (*)(PyObject *const *, Py_ssize_t, double *, \
               double *))PYGAMEAPI_GET_SLOT(base, 26))

#define pg_UintFromObj \
    (*(int (*)(PyObject *, Uint32 *))PYGAMEAPI_GET_SLOT(base, 8))

#define pg_UintFromObjIndex \
    (*(int (*)(PyObject *, int, Uint32 *))PYGAMEAPI_GET_SLOT(base, 9))

#define pg_mod_autoinit (*(int (*)(const char *))PYGAMEAPI_GET_SLOT(base, 10))

#define pg_mod_autoquit (*(void (*)(const char *))PYGAMEAPI_GET_SLOT(base, 11))

#define pg_RGBAFromObj \
    (*(int (*)(PyObject *, Uint8 *))PYGAMEAPI_GET_SLOT(base, 12))

#define pgBuffer_AsArrayInterface \
    (*(PyObject * (*)(Py_buffer *)) PYGAMEAPI_GET_SLOT(base, 13))

#define pgBuffer_AsArrayStruct \
    (*(PyObject * (*)(Py_buffer *)) PYGAMEAPI_GET_SLOT(base, 14))

#define pgObject_GetBuffer \
    (*(int (*)(PyObject *, pg_buffer *, int))PYGAMEAPI_GET_SLOT(base, 15))

#define pgBuffer_Release (*(void (*)(pg_buffer *))PYGAMEAPI_GET_SLOT(base, 16))

#define pgDict_AsBuffer \
    (*(int (*)(pg_buffer *, PyObject *, int))PYGAMEAPI_GET_SLOT(base, 17))

#define pgExc_BufferError ((PyObject *)PYGAMEAPI_GET_SLOT(base, 18))

#define pg_GetDefaultWindow \
    (*(SDL_Window * (*)(void)) PYGAMEAPI_GET_SLOT(base, 19))

#define pg_SetDefaultWindow \
    (*(void (*)(SDL_Window *))PYGAMEAPI_GET_SLOT(base, 20))

#define pg_GetDefaultWindowSurface \
    (*(pgSurfaceObject * (*)(void)) PYGAMEAPI_GET_SLOT(base, 21))

#define pg_SetDefaultWindowSurface \
    (*(void (*)(pgSurfaceObject *))PYGAMEAPI_GET_SLOT(base, 22))

#define pg_EnvShouldBlendAlphaSDL2 \
    (*(int (*)(void))PYGAMEAPI_GET_SLOT(base, 23))

#define pg_GetDefaultConvertFormat \
    (*(PG_PixelFormatEnum (*)(void))PYGAMEAPI_GET_SLOT(base, 27))

#define pg_SetDefaultConvertFormat \
    (*(void (*)(Uint32))PYGAMEAPI_GET_SLOT(base, 28))

#define pgObject_getRectHelper                                               \
    (*(PyObject * (*)(PyObject *, PyObject *const *, Py_ssize_t, PyObject *, \
                      char *)) PYGAMEAPI_GET_SLOT(base, 29))

#define import_pygame_base() IMPORT_PYGAME_MODULE(base)
#endif /* ~PYGAMEAPI_BASE_INTERNAL */

typedef struct {
    PyObject_HEAD SDL_Rect r;
    PyObject *weakreflist;
} pgRectObject;

typedef struct {
    PyObject_HEAD SDL_FRect r;
    PyObject *weakreflist;
} pgFRectObject;

#define pgRect_AsRect(x) (((pgRectObject *)x)->r)
#define pgFRect_AsRect(x) (((pgFRectObject *)x)->r)
#ifndef PYGAMEAPI_RECT_INTERNAL
#define pgRect_Type (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(rect, 0))

#define pgRect_Check(x) ((x)->ob_type == &pgRect_Type)
#define pgRect_New (*(PyObject * (*)(SDL_Rect *)) PYGAMEAPI_GET_SLOT(rect, 1))

#define pgRect_New4 \
    (*(PyObject * (*)(int, int, int, int)) PYGAMEAPI_GET_SLOT(rect, 2))

#define pgRect_FromObject \
    (*(SDL_Rect * (*)(PyObject *, SDL_Rect *)) PYGAMEAPI_GET_SLOT(rect, 3))

#define pgRect_Normalize (*(void (*)(SDL_Rect *))PYGAMEAPI_GET_SLOT(rect, 4))

#define pgFRect_Type (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(rect, 5))

#define pgFRect_Check(x) ((x)->ob_type == &pgFRect_Type)
#define pgFRect_New \
    (*(PyObject * (*)(SDL_FRect *)) PYGAMEAPI_GET_SLOT(rect, 6))

#define pgFRect_New4 \
    (*(PyObject * (*)(float, float, float, float)) PYGAMEAPI_GET_SLOT(rect, 7))

#define pgFRect_FromObject \
    (*(SDL_FRect * (*)(PyObject *, SDL_FRect *)) PYGAMEAPI_GET_SLOT(rect, 8))

#define pgFRect_Normalize (*(void (*)(SDL_FRect *))PYGAMEAPI_GET_SLOT(rect, 9))

#define import_pygame_rect() IMPORT_PYGAME_MODULE(rect)
#endif /* ~PYGAMEAPI_RECT_INTERNAL */

/*
 * JOYSTICK module
 */
typedef struct pgJoystickObject {
    PyObject_HEAD int id;
    SDL_Joystick *joy;

    /* Joysticks form an intrusive linked list.
     *
     * Note that we don't maintain refcounts for these so they are weakrefs
     * from the Python side.
     */
    struct pgJoystickObject *next;
    struct pgJoystickObject *prev;
} pgJoystickObject;

#define pgJoystick_AsID(x) (((pgJoystickObject *)x)->id)
#define pgJoystick_AsSDL(x) (((pgJoystickObject *)x)->joy)

#ifndef PYGAMEAPI_JOYSTICK_INTERNAL
#define pgJoystick_Type (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(joystick, 0))

#define pgJoystick_Check(x) ((x)->ob_type == &pgJoystick_Type)
#define pgJoystick_New (*(PyObject * (*)(int)) PYGAMEAPI_GET_SLOT(joystick, 1))
#define pgJoystick_GetDeviceIndexByInstanceID \
    (*(int (*)(int))PYGAMEAPI_GET_SLOT(joystick, 2))

#define import_pygame_joystick() IMPORT_PYGAME_MODULE(joystick)
#endif

/*
 * DISPLAY module
 */

typedef struct {
    Uint32 hw_available : 1;
    Uint32 wm_available : 1;
    Uint32 blit_hw : 1;
    Uint32 blit_hw_CC : 1;
    Uint32 blit_hw_A : 1;
    Uint32 blit_sw : 1;
    Uint32 blit_sw_CC : 1;
    Uint32 blit_sw_A : 1;
    Uint32 blit_fill : 1;
    Uint32 video_mem;
    SDL_PixelFormat *vfmt;
    SDL_PixelFormat vfmt_data;
    int current_w;
    int current_h;
} pg_VideoInfo;

typedef struct {
    PyObject_HEAD pg_VideoInfo info;
} pgVidInfoObject;

#define pgVidInfo_AsVidInfo(x) (((pgVidInfoObject *)x)->info)

#ifndef PYGAMEAPI_DISPLAY_INTERNAL
#define pgVidInfo_Type (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(display, 0))

#define pgVidInfo_Check(x) ((x)->ob_type == &pgVidInfo_Type)
#define pgVidInfo_New \
    (*(PyObject * (*)(pg_VideoInfo *)) PYGAMEAPI_GET_SLOT(display, 1))

#define import_pygame_display() IMPORT_PYGAME_MODULE(display)
#endif /* ~PYGAMEAPI_DISPLAY_INTERNAL */

/*
 * SURFACE module
 */
struct pgSubSurface_Data;
struct SDL_Surface;

typedef struct {
    PyObject_HEAD struct SDL_Surface *surf;
    int owner;
    struct pgSubSurface_Data *subsurface; /* ptr to subsurface data (if a
                                           * subsurface)*/
    PyObject *weakreflist;
    PyObject *locklist;
    PyObject *dependency;
} pgSurfaceObject;
#define pgSurface_AsSurface(x) (((pgSurfaceObject *)x)->surf)

#ifndef PYGAMEAPI_SURFACE_INTERNAL
#define pgSurface_Type (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(surface, 0))

#define pgSurface_Check(x) \
    (PyObject_IsInstance((x), (PyObject *)&pgSurface_Type))
#define pgSurface_New2                            \
    (*(pgSurfaceObject * (*)(SDL_Surface *, int)) \
         PYGAMEAPI_GET_SLOT(surface, 1))

#define pgSurface_SetSurface                                              \
    (*(int (*)(pgSurfaceObject *, SDL_Surface *, int))PYGAMEAPI_GET_SLOT( \
        surface, 3))

#define pgSurface_Blit                                                       \
    (*(int (*)(pgSurfaceObject *, pgSurfaceObject *, SDL_Rect *, SDL_Rect *, \
               int))PYGAMEAPI_GET_SLOT(surface, 2))

#define import_pygame_surface()         \
    do {                                \
        IMPORT_PYGAME_MODULE(surface);  \
        if (PyErr_Occurred() != NULL)   \
            break;                      \
        IMPORT_PYGAME_MODULE(surflock); \
    } while (0)

#define pgSurface_New(surface) pgSurface_New2((surface), 1)
#define pgSurface_NewNoOwn(surface) pgSurface_New2((surface), 0)

#endif /* ~PYGAMEAPI_SURFACE_INTERNAL */

/*
 * SURFLOCK module
 * auto imported/initialized by surface
 */
#ifndef PYGAMEAPI_SURFLOCK_INTERNAL
#define pgSurface_Prep(x) \
    if ((x)->subsurface)  \
    (*(*(void (*)(pgSurfaceObject *))PYGAMEAPI_GET_SLOT(surflock, 0)))(x)

#define pgSurface_Unprep(x) \
    if ((x)->subsurface)    \
    (*(*(void (*)(pgSurfaceObject *))PYGAMEAPI_GET_SLOT(surflock, 1)))(x)

#define pgSurface_Lock \
    (*(int (*)(pgSurfaceObject *))PYGAMEAPI_GET_SLOT(surflock, 2))

#define pgSurface_Unlock \
    (*(int (*)(pgSurfaceObject *))PYGAMEAPI_GET_SLOT(surflock, 3))

#define pgSurface_LockBy \
    (*(int (*)(pgSurfaceObject *, PyObject *))PYGAMEAPI_GET_SLOT(surflock, 4))

#define pgSurface_UnlockBy \
    (*(int (*)(pgSurfaceObject *, PyObject *))PYGAMEAPI_GET_SLOT(surflock, 5))
#endif

/*
 * EVENT module
 */
typedef struct pgEventObject pgEventObject;

#ifndef PYGAMEAPI_EVENT_INTERNAL
#define pgEvent_Type (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(event, 0))

#define pgEvent_Check(x) ((x)->ob_type == &pgEvent_Type)

#define pgEvent_New \
    (*(PyObject * (*)(SDL_Event *)) PYGAMEAPI_GET_SLOT(event, 1))

#define pg_post_event \
    (*(int (*)(Uint32, PyObject *))PYGAMEAPI_GET_SLOT(event, 2))

#define pg_post_event_dictproxy \
    (*(int (*)(Uint32, pgEventDictProxy *))PYGAMEAPI_GET_SLOT(event, 3))

#define pg_EnableKeyRepeat (*(int (*)(int, int))PYGAMEAPI_GET_SLOT(event, 4))

#define pg_GetKeyRepeat (*(void (*)(int *, int *))PYGAMEAPI_GET_SLOT(event, 5))

#define pgEvent_GetKeyDownInfo (*(char *(*)(void))PYGAMEAPI_GET_SLOT(event, 6))

#define pgEvent_GetKeyUpInfo (*(char *(*)(void))PYGAMEAPI_GET_SLOT(event, 7))

#define pgEvent_GetMouseButtonDownInfo \
    (*(char *(*)(void))PYGAMEAPI_GET_SLOT(event, 8))

#define pgEvent_GetMouseButtonUpInfo \
    (*(char *(*)(void))PYGAMEAPI_GET_SLOT(event, 9))

#define import_pygame_event() IMPORT_PYGAME_MODULE(event)
#endif

/*
 * RWOBJECT module
 * the rwobject are only needed for C side work, not accessible from python.
 */
#ifndef PYGAMEAPI_RWOBJECT_INTERNAL
#define pgRWops_FromObject \
    (*(SDL_RWops * (*)(PyObject *, char **)) PYGAMEAPI_GET_SLOT(rwobject, 0))

#define pgRWops_IsFileObject \
    (*(int (*)(SDL_RWops *))PYGAMEAPI_GET_SLOT(rwobject, 1))

#define pg_EncodeFilePath \
    (*(PyObject * (*)(PyObject *, PyObject *)) PYGAMEAPI_GET_SLOT(rwobject, 2))

#define pg_EncodeString                                                    \
    (*(PyObject * (*)(PyObject *, const char *, const char *, PyObject *)) \
         PYGAMEAPI_GET_SLOT(rwobject, 3))

#define pgRWops_FromFileObject \
    (*(SDL_RWops * (*)(PyObject *)) PYGAMEAPI_GET_SLOT(rwobject, 4))

#define import_pygame_rwobject() IMPORT_PYGAME_MODULE(rwobject)

#endif

/*
 * PixelArray module
 */
#ifndef PYGAMEAPI_PIXELARRAY_INTERNAL
#define PyPixelArray_Type ((PyTypeObject *)PYGAMEAPI_GET_SLOT(pixelarray, 0))

#define PyPixelArray_Check(x) ((x)->ob_type == &PyPixelArray_Type)
#define PyPixelArray_New (*(PyObject * (*)) PYGAMEAPI_GET_SLOT(pixelarray, 1))

#define import_pygame_pixelarray() IMPORT_PYGAME_MODULE(pixelarray)
#endif /* PYGAMEAPI_PIXELARRAY_INTERNAL */

/*
 * BufferProxy module
 */
typedef struct {
    PyObject_HEAD PyObject *obj; /* Wrapped object (parent)     */
    pg_buffer *pg_view_p;        /* For array interface export  */
    getbufferproc get_buffer;    /* pg_buffer get callback      */
    PyObject *dict;              /* Allow arbitrary attributes  */
    PyObject *weakrefs;          /* Reference cycles can happen */
} pgBufferProxyObject;

#ifndef PYGAMEAPI_BUFFERPROXY_INTERNAL
#define pgBufferProxy_Type \
    (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(bufferproxy, 0))

#define pgBufferProxy_Check(x) ((x)->ob_type == &pgBufferProxy_Type)
#define pgBufferProxy_New                         \
    (*(PyObject * (*)(PyObject *, getbufferproc)) \
         PYGAMEAPI_GET_SLOT(bufferproxy, 1))

#define pgBufferProxy_GetParent \
    (*(PyObject * (*)(PyObject *)) PYGAMEAPI_GET_SLOT(bufferproxy, 2))
#define pgBufferProxy_Trip \
    (*(int (*)(PyObject *))PYGAMEAPI_GET_SLOT(bufferproxy, 3))

#define import_pygame_bufferproxy() _IMPORT_PYGAME_MODULE(bufferproxy)
#endif /* ~PYGAMEAPI_BUFFERPROXY_INTERNAL */

/*
 * Color module
 */
typedef struct pgColorObject pgColorObject;

#ifndef PYGAMEAPI_COLOR_INTERNAL
#define pgColor_Type (*(PyObject *)PYGAMEAPI_GET_SLOT(color, 0))

#define pgColor_CheckExact(x) ((x)->ob_type == &pgColor_Type)
#define pgColor_New (*(PyObject * (*)(Uint8 *)) PYGAMEAPI_GET_SLOT(color, 1))

#define pgColor_NewLength \
    (*(PyObject * (*)(Uint8 *, Uint8)) PYGAMEAPI_GET_SLOT(color, 3))

#define pg_RGBAFromObjEx                                                    \
    (*(int (*)(PyObject *, Uint8 *, pgColorHandleFlags))PYGAMEAPI_GET_SLOT( \
        color, 2))

#define pg_MappedColorFromObj                       \
    (*(int (*)(PyObject *, SDL_Surface *, Uint32 *, \
               pgColorHandleFlags))PYGAMEAPI_GET_SLOT(color, 4))

#define pgColor_AsArray(x) (((pgColorObject *)x)->data)
#define pgColor_NumComponents(x) (((pgColorObject *)x)->len)

#define import_pygame_color() IMPORT_PYGAME_MODULE(color)
#endif /* PYGAMEAPI_COLOR_INTERNAL */

/*
 * Math module
 */
#ifndef PYGAMEAPI_MATH_INTERNAL
#define pgVector2_Check(x) \
    ((x)->ob_type == (PyTypeObject *)PYGAMEAPI_GET_SLOT(math, 0))

#define pgVector3_Check(x) \
    ((x)->ob_type == (PyTypeObject *)PYGAMEAPI_GET_SLOT(math, 1))
/*
#define pgVector2_New                                             \
    (*(PyObject*(*))  \
        PYGAMEAPI_GET_SLOT(PyGAME_C_API, 1))
*/
#define import_pygame_math() IMPORT_PYGAME_MODULE(math)
#endif /* PYGAMEAPI_MATH_INTERNAL */

#ifndef PYGAMEAPI_GEOMETRY_INTERNAL

#define import_pygame_geometry() IMPORT_PYGAME_MODULE(geometry)

#endif /* ~PYGAMEAPI_GEOMETRY_INTERNAL */

/*
 * Window module
 */
typedef struct {
    PyObject_HEAD SDL_Window *_win;
    SDL_bool _is_borrowed;
    pgSurfaceObject *surf;
    SDL_GLContext context;
} pgWindowObject;

#ifndef PYGAMEAPI_WINDOW_INTERNAL
#define pgWindow_Type (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(window, 0))
#define pgWindow_Check(x) \
    (PyObject_IsInstance((x), (PyObject *)&pgWindow_Type))
#define import_pygame_window() IMPORT_PYGAME_MODULE(window)
#endif

typedef struct pgTextureObject pgTextureObject;

/*
 * Render module
 */
typedef struct {
    PyObject_HEAD SDL_Renderer *renderer;
    pgWindowObject *window;
    pgTextureObject *target;
    SDL_bool _is_borrowed;
} pgRendererObject;

struct pgTextureObject {
    PyObject_HEAD SDL_Texture *texture;
    pgRendererObject *renderer;
    int width;
    int height;
};

typedef struct {
    PyObject_HEAD pgTextureObject *texture;
    pgRectObject *srcrect;
    pgColorObject *color;
    float angle;
    float alpha;
    SDL_bool has_origin;
    SDL_FPoint origin;
    SDL_bool flip_x;
    SDL_bool flip_y;
    SDL_BlendMode blend_mode;
} pgImageObject;

#ifndef PYGAMEAPI_RENDER_INTERNAL
#define pgRenderer_Type (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(_render, 0))
#define pgTexture_Type (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(_render, 1))
#define pgImage_Type (*(PyTypeObject *)PYGAMEAPI_GET_SLOT(_render, 2))
#define pgRenderer_Check(x) \
    (PyObject_IsInstance((x), (PyObject *)&pgRender_Type))
#define pgTexture_Check(x) \
    (PyObject_IsInstance((x), (PyObject *)&pgTexture_Type))
#define pgImage_Check(x) (PyObject_IsInstance((x), (PyObject *)&pgImage_Type))
#define import_pygame_render() IMPORT_PYGAME_MODULE(_render)
#endif

#define IMPORT_PYGAME_MODULE _IMPORT_PYGAME_MODULE

/*
 * base pygame API slots
 * disable slots with NO_PYGAME_C_API
 */
#ifdef PYGAME_H
PYGAMEAPI_DEFINE_SLOTS(base);
PYGAMEAPI_DEFINE_SLOTS(rect);
PYGAMEAPI_DEFINE_SLOTS(joystick);
PYGAMEAPI_DEFINE_SLOTS(display);
PYGAMEAPI_DEFINE_SLOTS(surface);
PYGAMEAPI_DEFINE_SLOTS(surflock);
PYGAMEAPI_DEFINE_SLOTS(event);
PYGAMEAPI_DEFINE_SLOTS(rwobject);
PYGAMEAPI_DEFINE_SLOTS(pixelarray);
PYGAMEAPI_DEFINE_SLOTS(bufferproxy);
PYGAMEAPI_DEFINE_SLOTS(color);
PYGAMEAPI_DEFINE_SLOTS(math);
PYGAMEAPI_DEFINE_SLOTS(window);
PYGAMEAPI_DEFINE_SLOTS(_render);
PYGAMEAPI_DEFINE_SLOTS(geometry);
#else /* ~PYGAME_H */
PYGAMEAPI_EXTERN_SLOTS(base);
PYGAMEAPI_EXTERN_SLOTS(rect);
PYGAMEAPI_EXTERN_SLOTS(joystick);
PYGAMEAPI_EXTERN_SLOTS(display);
PYGAMEAPI_EXTERN_SLOTS(surface);
PYGAMEAPI_EXTERN_SLOTS(surflock);
PYGAMEAPI_EXTERN_SLOTS(event);
PYGAMEAPI_EXTERN_SLOTS(rwobject);
PYGAMEAPI_EXTERN_SLOTS(pixelarray);
PYGAMEAPI_EXTERN_SLOTS(bufferproxy);
PYGAMEAPI_EXTERN_SLOTS(color);
PYGAMEAPI_EXTERN_SLOTS(math);
PYGAMEAPI_EXTERN_SLOTS(window);
PYGAMEAPI_EXTERN_SLOTS(_render);
PYGAMEAPI_EXTERN_SLOTS(geometry);

#endif /* ~PYGAME_H */

/*  Use the end of this file for other cross module inline utility
 *  functions There seems to be no good reason to stick to macro only
 *  functions in Python 3.
 */

#define SURF_INIT_CHECK(surf)                                           \
    {                                                                   \
        if (!surf) {                                                    \
            return RAISE(pgExc_SDLError, "Surface is not initialized"); \
        }                                                               \
    }

static PG_INLINE PyObject *
pg_tuple_couple_from_values_int(int val1, int val2)
{
    /* This function turns two input integers into a python tuple object.
     * Currently, 5th November 2022, this is faster than using Py_BuildValue
     * to do the same thing.
     */
    PyObject *tup = PyTuple_New(2);
    if (!tup) {
        return NULL;
    }

    PyObject *tmp = PyLong_FromLong(val1);
    if (!tmp) {
        Py_DECREF(tup);
        return NULL;
    }
    PyTuple_SET_ITEM(tup, 0, tmp);

    tmp = PyLong_FromLong(val2);
    if (!tmp) {
        Py_DECREF(tup);
        return NULL;
    }
    PyTuple_SET_ITEM(tup, 1, tmp);

    return tup;
}

static PG_INLINE PyObject *
pg_tuple_triple_from_values_int(int val1, int val2, int val3)
{
    /* This function turns three input integers into a python tuple object.
     * Currently, 5th November 2022, this is faster than using Py_BuildValue
     * to do the same thing.
     */
    PyObject *tup = PyTuple_New(3);
    if (!tup) {
        return NULL;
    }

    PyObject *tmp = PyLong_FromLong(val1);
    if (!tmp) {
        Py_DECREF(tup);
        return NULL;
    }
    PyTuple_SET_ITEM(tup, 0, tmp);

    tmp = PyLong_FromLong(val2);
    if (!tmp) {
        Py_DECREF(tup);
        return NULL;
    }
    PyTuple_SET_ITEM(tup, 1, tmp);

    tmp = PyLong_FromLong(val3);
    if (!tmp) {
        Py_DECREF(tup);
        return NULL;
    }
    PyTuple_SET_ITEM(tup, 2, tmp);

    return tup;
}

static PG_INLINE PyObject *
pg_tuple_couple_from_values_double(double val1, double val2)
{
    /* This function turns two input doubles into a python tuple object.
     * Currently, 5th November 2022, this is faster than using Py_BuildValue
     * to do the same thing.
     */
    PyObject *tuple = PyTuple_New(2);
    if (!tuple) {
        return NULL;
    }

    PyObject *tmp = PyFloat_FromDouble(val1);
    if (!tmp) {
        Py_DECREF(tuple);
        return NULL;
    }
    PyTuple_SET_ITEM(tuple, 0, tmp);

    tmp = PyFloat_FromDouble(val2);
    if (!tmp) {
        Py_DECREF(tuple);
        return NULL;
    }
    PyTuple_SET_ITEM(tuple, 1, tmp);

    return tuple;
}

static PG_INLINE PyObject *
pg_PointList_FromArrayDouble(double const *array, int arr_length)
{
    if (arr_length % 2) {
        return RAISE(PyExc_ValueError, "array length must be even");
    }

    int num_points = arr_length / 2;
    PyObject *sequence = PyList_New(num_points);
    if (!sequence) {
        return NULL;
    }

    int i;
    PyObject *point = NULL;
    for (i = 0; i < num_points; i++) {
        point =
            pg_tuple_couple_from_values_double(array[i * 2], array[i * 2 + 1]);
        if (!point) {
            Py_DECREF(sequence);
            return NULL;
        }
        PyList_SET_ITEM(sequence, i, point);
        point = NULL;
    }

    return sequence;
}

#if PY_VERSION_HEX >= 0x030C0000

#define PG_DECLARE_EXCEPTION_SAVER static PyObject *__cached_exception = NULL;

#define PG_SAVE_EXCEPTION __cached_exception = PyErr_GetRaisedException();

#define PG_UNSAVE_EXCEPTION                       \
    PyErr_SetRaisedException(__cached_exception); \
    __cached_exception = NULL;

#else

#define PG_DECLARE_EXCEPTION_SAVER                    \
    static PyObject *__cached_exception_type = NULL;  \
    static PyObject *__cached_exception_value = NULL; \
    static PyObject *__cached_exception_traceback = NULL;

#define PG_SAVE_EXCEPTION                                            \
    PyErr_Fetch(&__cached_exception_type, &__cached_exception_value, \
                &__cached_exception_traceback);

#define PG_UNSAVE_EXCEPTION                                          \
    PyErr_Restore(__cached_exception_type, __cached_exception_value, \
                  __cached_exception_traceback);                     \
    __cached_exception_type = NULL;                                  \
    __cached_exception_value = NULL;                                 \
    __cached_exception_traceback = NULL;

#endif

/* Slot counts.
 * Remember to keep these constants up to date.
 */

#define PYGAMEAPI_RECT_NUMSLOTS 10
#define PYGAMEAPI_JOYSTICK_NUMSLOTS 3
#define PYGAMEAPI_DISPLAY_NUMSLOTS 2
#define PYGAMEAPI_SURFACE_NUMSLOTS 4
#define PYGAMEAPI_SURFLOCK_NUMSLOTS 6
#define PYGAMEAPI_RWOBJECT_NUMSLOTS 5
#define PYGAMEAPI_PIXELARRAY_NUMSLOTS 2
#define PYGAMEAPI_COLOR_NUMSLOTS 5
#define PYGAMEAPI_MATH_NUMSLOTS 2
#define PYGAMEAPI_BASE_NUMSLOTS 30
#define PYGAMEAPI_EVENT_NUMSLOTS 10
#define PYGAMEAPI_WINDOW_NUMSLOTS 1
#define PYGAMEAPI_RENDER_NUMSLOTS 3
#define PYGAMEAPI_GEOMETRY_NUMSLOTS 2
#define PYGAMEAPI_BUFFERPROXY_NUMSLOTS 4

#endif /* _PYGAME_INTERNAL_H */
