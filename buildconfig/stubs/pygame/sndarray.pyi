from typing import Tuple

import numpy

from pygame.mixer import Sound

def array(sound: Sound) -> numpy.ndarray: ...
def samples(sound: Sound) -> numpy.ndarray: ...
def make_sound(array: numpy.ndarray) -> Sound: ...
# use_arraytype deprecated
# get_arraytype deprecated
# get_arraytypes deprecated
