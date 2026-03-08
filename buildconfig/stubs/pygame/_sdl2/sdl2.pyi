INIT_TIMER: int
INIT_AUDIO: int
INIT_VIDEO: int
INIT_JOYSTICK: int
INIT_HAPTIC: int
INIT_GAMECONTROLLER: int
INIT_EVENTS: int
INIT_NOPARACHUTE: int
INIT_EVERYTHING: int

class error(RuntimeError):
    def __init__(self, message: str | None = None) -> None: ...

def init_subsystem(flags: int) -> None: ...
