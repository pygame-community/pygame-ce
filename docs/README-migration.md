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
