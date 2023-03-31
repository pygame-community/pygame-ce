#if !defined(PGCOMPAT_H)
#define PGCOMPAT_H

#include <Python.h>

/* In CPython, Py_Exit finalises the python interpreter before calling C exit()
 * This does not exist on PyPy, so use exit() directly here */
#ifdef PYPY_VERSION
#define PG_EXIT(n) exit(n)
#else
#define PG_EXIT(n) Py_Exit(n)
#endif

/* define common types where SDL is not included */
#ifndef SDL_VERSION_ATLEAST
#ifdef _MSC_VER
typedef unsigned __int8 uint8_t;
typedef unsigned __int32 uint32_t;
#else
#include <stdint.h>
#endif
typedef uint32_t Uint32;
typedef uint8_t Uint8;
#endif /* no SDL */

#if defined(SDL_VERSION_ATLEAST)

#if SDL_VERSION_ATLEAST(2, 0, 18)
#define PG_GetTicks SDL_GetTicks64
#else
#define PG_GetTicks SDL_GetTicks
#endif /* SDL_VERSION_ATLEAST(2, 0, 18) */

#ifndef SDL_MOUSEWHEEL_FLIPPED
#define NO_SDL_MOUSEWHEEL_FLIPPED
#endif

#endif /* defined(SDL_VERSION_ATLEAST) */

#endif /* ~defined(PGCOMPAT_H) */
