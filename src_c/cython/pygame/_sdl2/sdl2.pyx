# cython: language_level=2
#

# pygame.error
class error(RuntimeError):
    def __init__(self, message=None):
        if message is None:
            message = PGSDL_GetError().decode('utf8')
        RuntimeError.__init__(self, message)




# for init_subsystem. Expose variables to python.
INIT_TIMER = _PGSDL_INIT_TIMER
INIT_AUDIO = _PGSDL_INIT_AUDIO
INIT_VIDEO = _PGSDL_INIT_VIDEO
INIT_JOYSTICK = _PGSDL_INIT_JOYSTICK
INIT_HAPTIC = _PGSDL_INIT_HAPTIC
INIT_GAMECONTROLLER = _PGSDL_INIT_GAMECONTROLLER
INIT_EVENTS = _PGSDL_INIT_EVENTS
# INIT_SENSOR is not part of the portable adapter contract.
INIT_NOPARACHUTE = _PGSDL_INIT_NOPARACHUTE
INIT_EVERYTHING = _PGSDL_INIT_EVERYTHING


# TODO: Not sure about exposing init_subsystem in pygame.
#       It would be useful if you wanted to use audio without SDL_mixer.

# https://wiki.libsdl.org/SDL_InitSubSystem
def init_subsystem(flags):
    """ Use this function to initialize specific subsystems.

    :param int flags: any of the flags used by.

        * INIT_TIMER timer subsystem
        * INIT_AUDIO audio subsystem
        * INIT_VIDEO video subsystem; automatically initializes the events subsystem
        * INIT_JOYSTICK joystick subsystem; automatically initializes the events subsystem
        * INIT_HAPTIC haptic (force feedback) subsystem
        * INIT_GAMECONTROLLER controller subsystem; automatically initializes the joystick subsystem
        * INIT_EVENTS events subsystem
        * INIT_EVERYTHING all of the above subsystems
        * INIT_NOPARACHUTE compatibility; this flag is ignored
    """
    if (PGSDL_InitSubSystem(flags) == -1):
        raise error()
