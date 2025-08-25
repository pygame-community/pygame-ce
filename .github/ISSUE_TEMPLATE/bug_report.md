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
pygame-ce 6.6.6 (SDL 2.30.3, Python 3.11.1)
Platform:		Windows-10-10.0.22631-SP0
System:			Windows
System Version:	10.0.22631
Processor:		AMD64 Family 23 Model 113 Stepping 0, AuthenticAMD
Architecture:	Bits: 64bit	Linkage: WindowsPE

Python:			    CPython 3.11.1 (tags/v3.11.1:a7a450f, Dec  6 2022, 19:58:39) [MSC v.1934 64 bit (AMD64)]
pygame version:		2.5.0.dev3
SDL versions:		Linked: 2.30.3	Compiled: 2.30.3
SDL Mixer versions:	Linked: 2.8.0	Compiled: 2.8.0
SDL Font versions:	Linked: 2.22.0	Compiled: 2.22.0
SDL Image versions:	Linked: 2.8.2	Compiled: 2.8.2
Freetype versions:	Linked: 2.11.1	Compiled: 2.11.1

Display Driver:		windows
Mixer Driver:		wasapi
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
if the bug is caused by a specific file (image, font, sound, level, please upload it as an attachment

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
paste other relevant logs or stack traces here, if applicable
```
