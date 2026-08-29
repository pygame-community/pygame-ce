#ifndef PYGAME_PGSDL_H
#define PYGAME_PGSDL_H

#include "pygame.h"

#ifndef PG_SDL3
#include <SDL_mixer.h>
#define PGSDL_INIT_GAMECONTROLLER SDL_INIT_GAMECONTROLLER
#define PGSDL_INIT_HAPTIC SDL_INIT_HAPTIC
#define PGSDL_INIT_NOPARACHUTE SDL_INIT_NOPARACHUTE
#else
#define PGSDL_INIT_GAMECONTROLLER SDL_INIT_GAMEPAD
#define PGSDL_INIT_HAPTIC 0
#define PGSDL_INIT_NOPARACHUTE 0
#endif

#define PGSDL_INIT_TIMER SDL_INIT_TIMER
#define PGSDL_INIT_AUDIO SDL_INIT_AUDIO
#define PGSDL_INIT_VIDEO SDL_INIT_VIDEO
#define PGSDL_INIT_JOYSTICK SDL_INIT_JOYSTICK
#define PGSDL_INIT_EVENTS SDL_INIT_EVENTS
#define PGSDL_INIT_EVERYTHING SDL_INIT_EVERYTHING

static inline const char *
PGSDL_GetError(void)
{
    return SDL_GetError();
}

static inline int
PGSDL_InitSubSystem(Uint32 flags)
{
#ifdef PG_SDL3
    return SDL_InitSubSystem(flags) ? 0 : -1;
#else
    return SDL_InitSubSystem(flags);
#endif
}

static inline void
PGSDL_QuitSubSystem(Uint32 flags)
{
    SDL_QuitSubSystem(flags);
}

static inline Uint32
PGSDL_WasInit(Uint32 flags)
{
    return SDL_WasInit(flags);
}

#endif