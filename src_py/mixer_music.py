import pygame._mixer_music
import pygame.event
from pygame._mixer_music import *  # pylint: disable=wildcard-import,unused-wildcard-import; lgtm[py/polluting-import]


def __endevent_callback(endevent):
    if Queue._Queue__playing_instance is not None and endevent == _music_endevent:
        Queue._Queue__playing_instance._Queue__endevent()


pygame._mixer_music._register_endevent_callback(__endevent_callback)
_music_endevent = pygame.event.custom_type()


class Queue:
    __playing_instance = None

    def __init__(self, filenames=None):
        self.filenames = filenames
        self.__index = 0
        self.__loops = 0
        self.__loop_count = 0
        self.__fade_ms = 0
        self.__playing = False
        self.__ended_paused = False
        self.__last_played = None

    @property
    def filenames(self):
        return self.__filenames.copy()

    @filenames.setter
    def filenames(self, v):
        self.__filenames = []
        self.__song_loops = {}
        for data in v:
            if isinstance(data, str):
                self.__filenames.append(data)
            else:
                fn, loops = data
                self.__filenames.append(fn)
                self.__song_loops[fn] = loops
        self.__index = 0

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, v):
        self.__index = v
        if self.__index < 0 or self.__index >= len(self.__filenames):
            raise IndexError("Music index out of range")

    def add(self, filename, loops=0):
        self.__filenames.append(filename)
        if loops != 0:
            self.__song_loops[filename] = loops

    def remove(self, filename):
        self.__filenames.remove(filename)
        if filename in self.__song_loops:
            del self.__song_loops[filename]
        if self.__index >= len(self.__filenames):
            self.__index = 0

    def pop(self, index):
        popped = self.__filenames.pop(index)
        if popped in self.__song_loops:
            del self.__song_loops[popped]
        if self.__index >= len(self.__filenames):
            self.__index = 0
        return popped

    def get_busy(self):
        return self.__playing

    def get_current(self):
        return self.__last_played

    def get_next(self):
        if len(self.__filenames) <= 0:
            return -1
        if not self.__ended_paused:
            next_index = self.__index + 1
        else:
            next_index = self.__index
        if next_index >= len(self.__filenames):
            next_index = (
                0 if self.__loop_count < self.__loops - 1 or self.__loops == -1 else -1
            )
        return next_index

    def play(self, loops=0, fade_ms=0, index=0):
        self.__loops = loops
        self.__loop_count = 0
        self.__index = index
        self.__fade_ms = fade_ms
        self.__ended_paused = False
        if self.__index < 0 or self.__index >= len(self.__filenames):
            raise IndexError("Music index out of range")
        self.__play_current()
        self.__playing = True

    def play_next(self, loop: bool = True):
        self.__index += 1
        if self.__index >= len(self.__filenames):
            if loop:
                self.__index = 0
            else:
                self.__index = len(self.__filenames) - 1
        self.__play_current()
        self.__ended_paused = False

    def play_previous(self, loop: bool = True):
        self.__index -= 1
        if self.__index < 0:
            if loop:
                self.__index = max(0, len(self.__filenames) - 1)
            else:
                self.__index = 0
        self.__play_current()
        self.__ended_paused = False

    def play_at(self, index: int):
        self.__index = index
        if self.__index < 0 or self.__index >= len(self.__filenames):
            raise IndexError("Music index out of range")
        self.__play_current()
        self.__ended_paused = False

    def stop(self):
        self.__playing = False

    def resume(self):
        if self.__ended_paused:
            self.__play_current()
        self.__ended_paused = False
        self.__playing = True

    def restart(self):
        self.play(self.__loops, self.__fade_ms, 0)

    def __play_current(self):
        if len(self.__filenames) <= 0:
            return
        filename = self.__filenames[self.__index]
        loops = 0
        if filename in self.__song_loops:
            loops = self.__song_loops[filename]
        self.__last_played = self.__index
        pygame.mixer.music.stop()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(loops, 0, self.__fade_ms)
        pygame.mixer.music.set_endevent(_music_endevent)
        if (
            Queue.__playing_instance is not self
            and Queue.__playing_instance is not None
        ):
            Queue.__playing_instance.stop()
        Queue.__playing_instance = self

    def __endevent(self):
        self.__last_played = -1
        self.__index += 1
        if self.__index >= len(self.__filenames):
            if self.__loop_count < self.__loops - 1 or self.__loops == -1:
                self.__index = 0
                self.__loop_count += 1
                if self.__playing:
                    self.__play_current()
                else:
                    self.__ended_paused = True
            else:
                self.__index = len(self.__filenames) - 1
                self.__playing = False
        else:
            if self.__playing:
                self.__play_current()
            else:
                self.__ended_paused = True
