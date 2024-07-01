from pygame import *  # pylint: disable=wildcard-import; lgtm[py/polluting-import]

set_warnings_filter(2)

# TODO: Should we initialize here?
# pygame.print_debug_info() gives more information afterwards,
# but are there any side-effects of doing this?
init()

print_debug_info()
