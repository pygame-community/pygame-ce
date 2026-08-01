# Migrating to pygame-ce 3.0

This document provides information on what you might expect to see differently between the legacy pygame-ce 2.x.x and pygame-ce 3.x.x version.

## Support Prompt

The pygame-ce support prompt (this guy: `pygame-ce 2.5.7 (SDL 2.32.10, Python 3.13.3)`) will remain present in 2.x.x pygame-ce versions, but
is removed in 3.x.x pygame-ce versions. It's been a long-time default printout of the library, but it's archaic and provides far less useful
information than `pygame.print_debug_info()` does, and so it's about time that it gets removed.
