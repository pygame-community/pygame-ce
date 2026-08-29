#ifndef PGCOMPAT_RECT_H
#define PGCOMPAT_RECT_H

#include <stdbool.h>

#ifdef PG_SDL3
#include <SDL3/SDL.h>
typedef bool PG_SDLBool;
#else
#include <SDL.h>
typedef SDL_bool PG_SDLBool;
#endif

/* SDL3 changed FRect edge semantics, so use pygame's compatibility version. */
#if defined(PG_SDL3) || !SDL_VERSION_ATLEAST(2, 0, 22)

PG_SDLBool
PG_IntersectFRectAndLine(SDL_FRect *rect, float *X1, float *Y1, float *X2,
                         float *Y2);
#else
#define PG_IntersectFRectAndLine SDL_IntersectFRectAndLine
#endif /* defined(PG_SDL3) || !SDL_VERSION_ATLEAST(2, 0, 22) */

#define pg_PyFloat_FromFloat(x) (PyFloat_FromDouble((double)x))

#endif /* PGCOMPAT_RECT_H */
