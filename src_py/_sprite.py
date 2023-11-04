import warnings

warnings.warn(
    "The ._sprite submodule is deprecated since 2.4.0. Please use pygame.sprite instead.",
    category=DeprecationWarning,
    stacklevel=2,
)

from pygame.sprite import (
    Sprite,
    DirtySprite,
    Group,
    GroupSingle,
    AbstractGroup,
    RenderClear,
    RenderPlain,
    RenderUpdates,
    LayeredUpdates,
    LayeredDirty,
    spritecollide,
    spritecollideany,
    collide_mask,
    collide_rect,
    collide_circle,
    collide_rect_ratio,
    collide_circle_ratio,
    groupcollide,
)
