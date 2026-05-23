#ifndef PGCOMPAT_RECT_H
#define PGCOMPAT_RECT_H
#ifdef PG_SDL3
#include <SDL3/SDL.h>
#else
#include <SDL.h>
#endif
/* SDL2's SDL_IntersectFRectAndLine has a -1 boundary bug for small float
 * rects (dimensions < 1.0). SDL3 has fixed this issue, so this custom
 * implementation is only used for SDL2. */
#if !SDL_VERSION_ATLEAST(3, 0, 0)
SDL_bool
PG_IntersectFRectAndLine(SDL_FRect *rect, float *X1, float *Y1, float *X2,
                         float *Y2);
#else
#define PG_IntersectFRectAndLine SDL_IntersectFRectAndLine
#endif /* !SDL_VERSION_ATLEAST(3, 0, 0) */
#define pg_PyFloat_FromFloat(x) (PyFloat_FromDouble((double)x))
#endif /* PGCOMPAT_RECT_H */
