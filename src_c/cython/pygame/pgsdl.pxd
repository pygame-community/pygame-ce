# cython: language_level=3str

cdef extern from "pgsdl.h" nogil:
    ctypedef unsigned char Uint8
    ctypedef unsigned short Uint16
    ctypedef unsigned int Uint32
    ctypedef unsigned long long Uint64
    ctypedef char Sint8
    ctypedef signed short Sint16
    ctypedef signed int Sint32
    ctypedef signed long long Sint64
    ctypedef int SDL_bool

    const char *PGSDL_GetError()
    int PGSDL_InitSubSystem(Uint32 flags)
    void PGSDL_QuitSubSystem(Uint32 flags)
    Uint32 PGSDL_WasInit(Uint32 flags)

    cdef int _PGSDL_INIT_TIMER "PGSDL_INIT_TIMER"
    cdef int _PGSDL_INIT_AUDIO "PGSDL_INIT_AUDIO"
    cdef int _PGSDL_INIT_VIDEO "PGSDL_INIT_VIDEO"
    cdef int _PGSDL_INIT_JOYSTICK "PGSDL_INIT_JOYSTICK"
    cdef int _PGSDL_INIT_HAPTIC "PGSDL_INIT_HAPTIC"
    cdef int _PGSDL_INIT_GAMECONTROLLER "PGSDL_INIT_GAMECONTROLLER"
    cdef int _PGSDL_INIT_EVENTS "PGSDL_INIT_EVENTS"
    cdef int _PGSDL_INIT_NOPARACHUTE "PGSDL_INIT_NOPARACHUTE"
    cdef int _PGSDL_INIT_EVERYTHING "PGSDL_INIT_EVERYTHING"