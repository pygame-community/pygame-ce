import pygame._mixer_music
import pygame.event
from pygame._mixer_music import *
"""(
    load,
    unload,
    play,
    rewind,
    stop,
    pause,
    unpause,
    fadeout,
    get_volume,
    set_volume,
    get_busy,
    set_pos,
    get_pos,
    queue,
    set_endevent,
    get_endevent,
    get_metadata,
)"""


def __endevent_callback(endevent):
    print(endevent)
    if Queue.__playing_instance is not None:
        Queue.__playing_instance._Queue__endevent(endevent)


pygame._mixer_music._register_endevent_callback(__endevent_callback)


# fix loops
class Queue:
    __playing_instance = None

    def __init__(self, filenames=None):
        self.filenames = filenames
        self.__index = 0
        self.__loops = 0
        self.__loop_count = 0
        self.__fade_ms = 0
        self.__endevent_code = pygame.event.custom_type()
        self.__playing = True
        self.__ended_paused = False

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

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, v):
        self.__index = v
        if self.__index < 0 or self.__index >= len(self.__filenames):
            # raise
            ...
        if self.__playing:
            self.__play_current()  # check

    def get_busy(self):
        return self.__playing

    def get_next(self):
        if len(self.__filenames) <= 0:
            return -1
        next_index = self.__index + 1
        if next_index >= self.__filenames:
            next_index = 0
        return next_index

    def play(self, loops=0, fade_ms=0, index=0):
        self.__loops = loops
        self.__loop_count = 0
        self.__index = index
        self.__fade_ms = fade_ms
        if self.__index < 0 or self.__index >= len(self.__filenames):
            # raise
            ...
        self.__play_current()

    def stop(self):
        self.__playing = False

    def resume(self):
        if self.__ended_paused:
            self.__play_current()
        self.__ended_paused = False

    def next(self):
        self.__index += 1
        if self.__index >= len(self.__filenames):
            self.__index = 0
        if self.__playing:
            self.__play_current()

    def previous(self):
        self.__index -= 1
        if self.__index < 0:
            self.__index = len(self.__filenames) - 1
        if self.__playing:
            self.__play_current()

    def restart(self):
        self.play(self.__loops, 0, self.__fade_ms, 0)

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

    def __play_current(self):
        if len(self.__filenames) <= 0:
            return
        filename = self.__filenames[self.__index]
        loops = 0
        if filename in self.__song_loops:
            loops = self.__song_loops[filename]
        pygame.mixer.music.stop()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(loops, 0, self.__fade_ms)
        pygame.mixer.music.set_endevent(self.__endevent_code)
        self.__playing = True
        if Queue.__playing_instance is not None:
            Queue.__playing_instance.stop()
        Queue.__playing_instance = self

    def __endevent(self, event):
        if event == self.__endevent_code:
            self.__index += 1
            if self.__index >= len(self.__filenames):
                if self.__loop_count < self.__loops or self.__loops == -1:
                    self.__index = 0
                    self.__loop_count += 1
                    if self.__playing:
                        self.__play_current()
                    else:
                        self.__ended_paused = True
                else:
                    self.__index = len(self.__filenames) - 1
            else:
                if self.__playing:
                    self.__play_current()
                else:
                    self.__ended_paused = True
