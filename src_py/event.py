from pygame._event import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]
from pygame.constants import USEREVENT, NUMEVENTS
from pygame.base import error


_is_init = False
_custom_event = USEREVENT + 1


def init():
    global _is_init

    _internal_mod_init()

    _is_init = True


def quit():
    global _is_init, _custom_event

    # The main reason for _custom_event to be reset here is so we can have a unit test that checks if pygame.event.custom_type() stops returning new types when they are finished, without that test preventing further tests from getting a custom event type.
    _custom_event = USEREVENT + 1
    _internal_mod_quit()

    _is_init = False


def custom_type():
    """custom_type() -> int\nmake custom user event type"""
    global _custom_event

    if _custom_event < NUMEVENTS:
        _custom_event += 1
        return _custom_event - 1
    else:
        raise error("pygame.event.custom_type made too many event types.")
