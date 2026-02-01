#ifndef _PG_BASE_AUDIO_H
#define _PG_BASE_AUDIO_H

#include "pygame.h"

/* SHARED DEFINITIONS FOR OTHER MODULES TO BE ABLE TO SEE. */

typedef struct {
    PyObject_HEAD SDL_AudioDeviceID devid;
} PGAudioDeviceStateObject;

typedef struct {
    PyObject_HEAD SDL_AudioStream *stream;
} PGAudioStreamStateObject;

#endif
