"""pygame module for clipboard support.

**EXPERIMENTAL!**: This API may change or disappear in later pygame releases. If
you use this, your code may break with the next pygame release.

The scrap module is for transferring data to/from the clipboard. This allows for
transferring of strings between pygame and other applications. Currently, only strings
are supported with the ``scrap.put_text``, ``scrap.get_text``, and ``scrap.has_text``
functions. All other functions are deprecated as of pygame 2.2.0 and will be removed
in a future release of pygame.

.. note:: ``scrap.put_text``, ``scrap.get_text``, and ``scrap.has_text`` use the same
   clipboard as the rest of the current API, but only strings are compatible with the
   new API as of right now.
"""

from typing_extensions import (
    Buffer,  # added in 3.12,
    deprecated,  # added in 3.13
)

def put_text(text: str, /) -> None:
    """
    Places text into the clipboard.

    Places the input text into the clipboard. The data should be a string.
    This is the same clipboard as the legacy scrap API when using ``SCRAP_TEXT``.

    :raises pygame.error: if video mode has not been set_mode

    .. note:: ``pygame.display.set_mode()`` should be called before using the ``scrap`` module

    .. versionadded:: 2.2.0
    """

def get_text() -> str:
    """
    Gets text from the clipboard.

    Gets text from the clipboard and returns it. If the clipboard is empty,
    returns an empty string. This is the same clipboard as the legacy scrap
    API when using ``SCRAP_TEXT``.

    .. versionadded:: 2.2.0
    """

def has_text() -> bool:
    """
    Checks if text is in the clipboard.

    Returns ``True`` if the clipboard has a string, otherwise returns ``False``.
    This is the same clipboard as the legacy scrap API when using ``SCRAP_TEXT``.

    .. versionadded:: 2.2.0
    """

@deprecated("since 2.2.0. Use the new API instead, which only requires display init")
def init() -> None: ...
@deprecated("since 2.2.0. Use the new API instead, which doesn't require scrap init")
def get_init() -> bool: ...
@deprecated("since 2.2.0. Use the new API instead: `pygame.scrap.get_text`")
def get(data_type: str, /) -> bytes | None: ...
@deprecated("since 2.2.0. Use the new API instead, which only supports strings")
def get_types() -> list[str]: ...
@deprecated("since 2.2.0. Use the new API instead: `pygame.scrap.put_text`")
def put(data_type: str, data: Buffer, /) -> None: ...
@deprecated("since 2.2.0. Use the new API instead: `pygame.scrap.has_text`")
def contains(data_type: str, /) -> bool: ...
@deprecated("since 2.2.0. Use the new API instead, which uses system clipboard")
def lost() -> bool: ...
@deprecated("since 2.2.0. Use the new API instead, which only supports strings")
def set_mode(mode: int, /) -> None: ...
