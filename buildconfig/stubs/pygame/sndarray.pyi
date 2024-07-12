from typing import Tuple

import numpy

from pygame.mixer import Sound

def array(sound: Sound) -> numpy.ndarray: ...
def samples(sound: Sound) -> numpy.ndarray: ...
def make_sound(array: numpy.ndarray) -> Sound: ...
def use_arraytype(arraytype: str) -> Sound:"""Deprecated. Only numpy is supported"""
def get_arraytype() -> str:"""Deprecated. Only numpy is supported"""
def get_arraytypes() -> Tuple[str]:"""Deprecated. Only numpy is supported"""
