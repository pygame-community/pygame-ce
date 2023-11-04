import warnings

warnings.warn(
    "The ._sprite submodule is deprecated. Please use pygame.sprite instead.",
    category=DeprecationWarning,
    stacklevel=2,
)

from pygame.sprite import *
