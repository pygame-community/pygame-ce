---
name: 🐛 Guided bug report
about: A template to help you create a bug report to improve Pygame! Useful if this is your first time reporting an issue.
title: ''
labels: bug
assignees: ''


---


**Environment:**

If possible, please include the output of `pygame.print_debug_info()` from your program in your bug report. It looks something
like this:

```
Platform:               Linux-6.12.57+deb13-amd64-x86_64-with-glibc2.41
System:                 Linux
System Version:         #1 SMP PREEMPT_DYNAMIC Debian 6.12.57-1 (2025-11-05)
Processor:                      SSE2: Yes       AVX2: Yes       NEON: No
Architecture:           Bits: 64bit     Linkage: ELF

Python:                 CPython 3.13.7 (main, Sep 24 2025, 05:12:25) [GCC 14.2.0]
GIL Enabled:            True
pygame version:         2.5.6
SDL versions:           Linked: 2.32.10 Compiled: 2.32.10
SDL Mixer versions:     Linked: 2.8.1   Compiled: 2.8.1
SDL Font versions:      Linked: 2.24.0  Compiled: 2.24.0
SDL Image versions:     Linked: 2.8.8   Compiled: 2.8.8
Freetype versions:      Linked: 2.13.3  Compiled: 2.13.3

Display Driver:         Display Not Initialized
Mixer Driver:           Mixer Not Initialized
```
If you can't get the debug output, any of the environment details included in it that you do know would be useful
in diagnosing the issue & helping you.

Other environment details, not included in `print_debug_info()`, that might help:
- **Relevant hardware** (e.g. if reporting a bug about a controller, tell us the brand & name of it):

**Current behavior:**

Describe how the bug manifests.

**Expected behavior:**

A clear and concise description of what you expected to happen.

**Screenshots**

If applicable, copy and paste screenshots to help explain your problem.

**Steps to reproduce:**

Please explain the steps required to duplicate the issue, especially if you are able to provide a sample application.
If the bug is caused by a specific file (image, font, sound, level ...etc) please upload it as an attachment.

1.
2.
3.

**Test code**

If possible add a simple test program that shows the problem described in this report.
```
import pygame
pygame.init()
print("Hello, world")
```

**Stack trace/error output/other error logs**

```
Paste other relevant logs or stack traces here, if applicable
```
