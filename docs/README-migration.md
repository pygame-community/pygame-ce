# Migrating to pygame-ce 3.0

This document provides information on what you might expect to see differently
between pygame-ce 2.x.x and pygame-ce 3.x.x. Unless otherwise noted in
documentation, none of these adjustments will apply to 2.x.x versions.

## Support Prompt

The pygame-ce support prompt, as well as the environment variable to disable it,
will be removed in 3.x.x pygame-ce versions. It's been a long-time default
printout of the library, but it is archaic and provides far less useful
information than `pygame.print_debug_info()` does, and so it's about time that
it gets removed.

So, users will have to say goodbye to their old companion

`pygame-ce 3.0.0.dev1 (SDL 3.4.0, Python 3.13.3)`

and the `PYGAME_HIDE_SUPPORT_PROMPT` environment variable.

## Build System

The legacy setup.py-based buildconfig has been removed; the meson-python
build backend has been the only supported build system for some time.

## Miscellaneous Function Changes

### print_debug_info
Removed the `filename` argument and added `get_debug_info` to get the raw string.

## `Rect`

### `__contains__` (`value in rect`)
Removed the undocumented `__contains__` functionality to check if one rect is completely inside another rect. Use the `contains()` method instead. (The original behavior of checking if the value is a coordinate or dimension is preserved.)

## `__contains__` of `Color`, `Vector2`, `Vector3`, `Rect`, `FRect`
Removed the explicit `__contains__` methods; Python will now fall back to using `__iter__` when using the `in` operator on these. \
`__contains__` can no longer be accessed directly as a method. \
The membership operation for these classes will no longer raise `TypeError` on objects of unexpected types. \
Certain equivalencies such as between whole number floats and integers now result in `True` for membership checking.
