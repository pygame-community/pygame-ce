import math
from typing import Any

import pygame
from pygame import _audio, _sdl3_mixer
from pygame.typing import FileLike

"""
This file is a compatibility layer for the pygame2 mixer and mixer.music
modules built on top of ports of SDL3's audio and SDL3_mixer.

In pygame-ce 2.0, this file is NOT relevant, and is NOT included in the
distribution. If you're looking for that code, see mixer.c and music.c.

It is not perfect or exact!
- There's something up with audio stuttering in some cases, I think it
  needs to be adjusted to be less proscriptive about audio spec when
  allowedchanges allows.
- I think the volume is messed up if you have a channel volume and a
  sound volume
- I couldn't get the buffer protocol working to my satisfaction, despite
  effort
- Apparently the current system supports pygame.mixer.Sound(sound_inst),
  which I think no one knew about, given feature request for sound.copy
- I think in pygame2, channels can be different objects and refer to the
  same underlying resource, this does not work like that. A channel = the
  channel (they are singletons)
- There a couple of TODOs throughout the code.

However, I believe this code will handle the vast majority of pygame-ce 2
projects in its current state.

------------------------

In the future, this module should also export the SDL3 mixer objects.
This will be accomplished with a dual initialization system. If the user
does anything to indicate that they are using the old paradigm, it should
come up to support that.

If mixer.pre_init is called, or mixer.init is called with arguments, that
indicates compat is needed. In this case, mixer.init would then know to
initialize the compat resources (the channels, the Mixer playback device).

Similarly, if the mixer module has already been initialized without compat
resources, any instantiation of a Sound, Channel, or calls to a music
interface should automatically bring up the compat resources and then
proceed.
"""


class MixerInternals:
    default_frequency = 44100
    default_size = -16
    default_channels = 2
    default_chunksize = 512
    default_allowedchanges = 5

    request_frequency = default_frequency
    request_size = default_size
    request_channels = default_channels
    request_chunksize = default_chunksize
    request_allowedchanges = default_allowedchanges
    request_device = None

    allow_channels_change = 0x4

    initialized = False
    # All Sound() audio is loaded into this format, if different than actual
    # mixer.spec it will be converted by SDL_mixer at runtime.
    mixer_buf_spec: _audio.AudioSpec | None = None
    mixer: _sdl3_mixer.Mixer | None = None
    channels: list["Channel"] = []
    reserved_channels = 0
    soundfount: str | None = None

    def init_check():
        if not MixerInternals.initialized:
            raise pygame.error("mixer not initialized")


def init(
    frequency: int = 0,
    size: int = 0,
    channels: int = 0,
    buffer: int = 0,
    devicename: str | None = None,
    allowedchanges: int = -1,
) -> None:
    if MixerInternals.initialized:
        return

    if frequency == 0:
        frequency = MixerInternals.request_frequency
    if size == 0:
        size = MixerInternals.request_size
    if allowedchanges == -1:
        allowedchanges = MixerInternals.request_allowedchanges
    if channels == 0:
        channels = MixerInternals.request_channels

    if allowedchanges & MixerInternals.allow_channels_change:
        if channels <= 1:
            channels = 1
        elif channels <= 3:
            channels = 2
        elif channels <= 5:
            channels = 4
        else:
            channels = 6
    else:
        if channels not in (1, 2, 4, 6):
            raise pygame.error("'channels' must be in 1, 2, 4, or 6")

    chunk = buffer
    if chunk == 0:
        chunk = MixerInternals.request_chunksize

    if devicename is None:
        devicename = MixerInternals.request_device

    if size == 8:
        fmt = _audio.U8
    elif size == -8:
        fmt = _audio.S8
    # 16 -> U16 not available in SDL3
    elif size == -16:
        fmt = _audio.S16
    elif size == 32:
        fmt = _audio.F32
    else:
        raise ValueError(f"Unsupported size {size}")

    # Make chunk a power of 2
    chunk = max(1 << (chunk - 1).bit_length(), 256)

    # TODO: driver envs

    _sdl3_mixer.init()
    _audio.init()

    mixer_spec = _audio.AudioSpec(fmt, channels, frequency)

    mixer_device = _audio.DEFAULT_PLAYBACK_DEVICE
    if devicename is not None:
        potential_devices = [
            device
            for device in _audio.get_playback_devices()
            if device.name == devicename
        ]
        if potential_devices:
            mixer_device = potential_devices[0]

    MixerInternals.mixer_buf_spec = mixer_spec
    MixerInternals.mixer = _sdl3_mixer.Mixer(mixer_device, mixer_spec)
    MixerInternals.channels = [Channel._allocate(i) for i in range(8)]
    MixerInternals.reserved_channels = 0

    music._init()

    MixerInternals.initialized = True


def pre_init(
    frequency: int = 0,
    size: int = 0,
    channels: int = 0,
    buffer: int = 0,
    devicename: str | None = None,
    allowedchanges: int = -1,
) -> None:
    if frequency != 0:
        MixerInternals.request_frequency = frequency
    else:
        MixerInternals.request_frequency = MixerInternals.default_frequency

    if size != 0:
        MixerInternals.request_size = size
    else:
        MixerInternals.request_size = MixerInternals.default_size

    if channels != 0:
        MixerInternals.request_channels = channels
    else:
        MixerInternals.request_channels = MixerInternals.default_channels

    if buffer != 0:
        MixerInternals.request_chunksize = buffer
    else:
        MixerInternals.request_chunksize = MixerInternals.default_chunksize

    MixerInternals.request_device = devicename

    if allowedchanges != -1:
        MixerInternals.request_allowedchanges = allowedchanges
    else:
        MixerInternals.request_allowedchanges = MixerInternals.default_allowedchanges


def quit() -> None:
    MixerInternals.initialized = False
    MixerInternals.mixer = None
    MixerInternals.channels = []
    music._quit()


def get_init() -> tuple[int, int, int]:
    if not MixerInternals.initialized:
        return None

    mix_spec = MixerInternals.mixer_buf_spec
    realform = (
        -mix_spec.format.bitsize
        if mix_spec.format.is_signed
        else mix_spec.format.bitsize
    )

    return (mix_spec.frequency, realform, mix_spec.channels)


def get_driver() -> str:
    MixerInternals.init_check()
    return _audio.get_current_driver()


def set_num_channels(count: int, /) -> None:
    MixerInternals.init_check()

    # TODO: lock
    channels = MixerInternals.channels

    if len(channels) > count:
        channels = channels[:count]
    else:
        channels = channels + [
            Channel._allocate(i) for i in range(len(channels), count)
        ]

    MixerInternals.channels = channels


def get_num_channels() -> int:
    MixerInternals.init_check()

    return len(MixerInternals.channels)


def set_reserved(count: int, /) -> int:
    MixerInternals.init_check()

    if count < 0:
        count = 0

    num_channels = get_num_channels()
    if count > num_channels:
        count = num_channels

    MixerInternals.reserved_channels = count
    return count


def find_channel(force: bool = False):
    MixerInternals.init_check()

    # TODO lock?
    for channel in MixerInternals.channels:
        if not channel.get_busy():
            return channel

    if force:
        return sorted(MixerInternals.channels, key=lambda ch: ch._start_time)[0]
    return None


def set_soundfont(paths: str | None = None, /) -> None:
    MixerInternals.init_check()

    # TODO: thread this through SDL_mixer.decoder.fluidsynth.soundfont_path
    # on load
    if paths is not None and not isinstance(paths, str):
        raise TypeError("Must pass string or None to set_soundfont")

    if paths == "":
        paths = None

    MixerInternals.soundfount = paths


def get_soundfont() -> str | None:
    MixerInternals.init_check()

    return MixerInternals.soundfount


# TODO: missing methods
# stop
# pause
# unpause
# fadeout
# get_busy


get_sdl_mixer_version = _sdl3_mixer.get_sdl_mixer_version


class Sound:
    def __init__(self, *args, **kwargs) -> None:
        MixerInternals.init_check()

        obj = None
        file = None
        buffer = None
        array = None

        audio_buffer = None

        if args:
            if kwargs or len(args) != 1:
                raise TypeError("Sound takes either 1 positional or 1 keyword argument")
            obj = args[0]

            if isinstance(obj, str) or hasattr(obj, "__fspath__"):
                file = obj
                obj = None
            else:
                file = obj
                buffer = obj
        elif kwargs:
            if len(kwargs) != 1:
                raise TypeError("Sound takes either 1 positional or 1 keyword argument")
            file = kwargs.get("file")
            buffer = kwargs.get("buffer")
            array = kwargs.get("array")
            if file is None and buffer is None and array is None:
                raise TypeError(f"Unrecognized keyword argument '{next(iter(kwargs))}'")
            if isinstance(buffer, str):
                raise TypeError("Unicode object not allowed as buffer object")
        else:
            raise TypeError("Sound takes either 1 positional or 1 keyword argument")

        if file is not None:
            audio_decoder = None
            try:
                audio_decoder = _sdl3_mixer.AudioDecoder(file)
            except Exception as e:
                # use 'buffer' as fallback for single arg
                if obj is None:
                    raise e

            if audio_decoder is not None:
                audio_buffer = audio_decoder.decode(MixerInternals.mixer_buf_spec)

        if audio_buffer is None and buffer is not None:
            memory_viewed = False
            try:
                audio_buffer = memoryview(buffer)
                memory_viewed = True
            except TypeError:
                if obj is not None:
                    pass
                else:
                    raise TypeError(
                        f"Expected object with buffer interface: got a {type(buffer).__name__}"
                    )

            if memory_viewed:
                audio_buffer = bytes(audio_buffer)

        if audio_buffer is None and array is not None:
            audio_buffer = self._buf_from_array(array)

        if audio_buffer is None:
            if obj is None:
                raise TypeError("Unrecognized argument")
            else:
                raise TypeError(f"Unrecognized argument (type {type(obj).__name__})")

        self._buffer = audio_buffer
        self._audio = _sdl3_mixer.Audio.from_raw(
            self._buffer, MixerInternals.mixer_buf_spec, MixerInternals.mixer
        )

        self._tag = str(id(self))
        self._volume = 1.0

    def _buf_from_array(self, array) -> bytes:
        """This is based on mixer.c _chunk_from_array, which comes with its
        own warning:
        TODO: This is taken from _numericsndarray without additions.
        * So this should be extended to properly handle integer sign
        * and byte order. These changes will not be backward compatible.
        """

        channels = MixerInternals.mixer_buf_spec.channels
        itemsize = MixerInternals.mixer_buf_spec.format.bytesize

        mv = memoryview(bytes(array))

        if channels == 1:
            if mv.ndim != 1:
                raise ValueError("Array must be 1-dimensional for mono mixer")
        else:
            if mv.ndim != 2:
                raise ValueError("Array must be 2-dimensional for stereo mixer")
            if mv.shape[1] != channels:
                raise ValueError("Array depth must match number of mixer channels")

        if mv.itemsize not in (1, 2, 4):
            raise ValueError(f"Unsupported integer size {mv.itemsize}")

        # Reinterpret raw memory as native-endian unsigned words, flattened row-major
        # (matches the *(Uint8/16/32 *) reads; sign/endian ignored, per the C TODO).
        ucode = {1: "B", 2: "H", 4: "I"}[mv.itemsize]
        samples = mv.cast("B").cast(ucode)  # flat unsigned words

        if itemsize == 1:
            out = bytearray(len(samples))
            for i, v in enumerate(samples):
                out[i] = v & 0xFF  # low byte
        # following C implementation, we assume 16 bit (2 byte) here even though
        # it could be 32 bit as well.
        elif mv.itemsize == 1:
            out = bytearray(len(samples) * 2)
            ov = memoryview(out).cast("H")
            for i, v in enumerate(samples):
                # promote 8 bit to 16 bit in special case
                ov[i] = (v << 8) & 0xFFFF
        else:
            out = bytearray(len(samples) * 2)
            ov = memoryview(out).cast("H")
            for i, v in enumerate(samples):
                # convert 2/4 byte values to 2 bytes
                ov[i] = v & 0xFFFF

        return bytes(out)

    def play(
        self,
        loops: int = 0,
        maxtime: int = -1,
        fade_ms: int = -1,
    ) -> "Channel":
        MixerInternals.init_check()
        selected_channel: Channel | None = None

        # TODO lock
        for channel in MixerInternals.channels[MixerInternals.reserved_channels :]:
            if not channel.get_busy():
                selected_channel = channel
                break

        if selected_channel is None:
            return None

        selected_channel.play(self, loops, maxtime, fade_ms)
        return selected_channel

    def stop(self) -> None:
        MixerInternals.init_check()
        for channel in MixerInternals.channels:
            if channel.get_sound() is self:
                channel.stop()

    def fadeout(self, time: int, /) -> None:
        MixerInternals.init_check()
        for channel in MixerInternals.channels:
            if channel.get_sound() is self:
                channel.fadeout(time)

    def set_volume(self, value: float, /) -> None:
        MixerInternals.init_check()

        # value < 0 won't change volume
        if value < 0.0:
            return

        # SDL3_mixer supports boosting gain, but Sound didn't,
        # so lets be consistent.
        if value > 1.0:
            value = 1.0

        self._volume = value
        MixerInternals.mixer.set_tag_gain(self._tag, value)

    def get_volume(self) -> float:
        MixerInternals.init_check()
        return self._volume

    def get_length(self) -> float:
        MixerInternals.init_check()

        # Why not just use float(self._audio.duration_ms) / 1000 ?
        # The existing test wants it to be higher precision than integer
        # milliseconds.
        return self._audio.duration_frames / MixerInternals.mixer_buf_spec.frequency

    def get_raw(self) -> bytes:
        MixerInternals.init_check()
        return self._buffer

    def copy(self):
        MixerInternals.init_check()
        new_sound = self.__class__(buffer=self._buffer)
        new_sound.set_volume(self.get_volume())
        return new_sound

    def __copy__(self):
        return self.copy()

    def get_num_channels(self):
        MixerInternals.init_check()
        return sum(
            1 for channel in MixerInternals.channels if channel.get_sound() is self
        )

    @property
    def _samples_address(self) -> int:
        MixerInternals.init_check()
        return pygame.BufferProxy(self._buffer).__array_interface__["data"][0]

    @property
    def __array_interface__(self) -> dict[str, Any]:
        audio_spec = self._audio.spec
        audio_format = audio_spec.format

        channels = audio_spec.channels
        itemsize = audio_format.bytesize

        if channels > 1:
            shape = (self._audio.duration_frames, channels)
            strides = (channels * itemsize, itemsize)
        else:
            shape = (self._audio.duration_frames,)
            strides = (itemsize,)

        if audio_format.is_int and audio_format.is_signed:
            typekind = "i"
        elif audio_format.is_int and audio_format.is_unsigned:
            typekind = "u"
        elif audio_format.is_float:
            typekind = "f"
        else:
            raise pygame.error(
                f"Pygame bug (mixer.Sound): unknown mixer format {audio_format}"
            )

        if itemsize == 1:
            byteorder = "|"
        elif audio_format.is_big_endian:
            byteorder = ">"
        elif audio_format.is_little_endian:
            byteorder = "<"
        else:
            raise pygame.error(
                f"Pygame bug (mixer.Sound): unknown mixer format {audio_format}"
            )

        return {
            "version": 3,
            "typestr": f"{byteorder}{typekind}{itemsize}",
            "shape": shape,
            "strides": strides,
            "data": (
                pygame.BufferProxy(self._buffer).__array_interface__["data"][0],
                False,
            ),
        }

    def __bytes__(self):
        return self._buffer


class Channel:
    def __new__(cls, id: int) -> "Channel":
        # Users don't construct channels, they retrieve one out of the
        # preallocated MixerInternals.channels pool by index. The real
        # allocation happens in _allocate (used internally by the mixer).
        MixerInternals.init_check()

        channels = MixerInternals.channels
        if not isinstance(id, int):
            raise TypeError(
                f"'{type(id).__name__}'object cannot be interpreted as an integer"
            )
        if id < 0 or id >= len(channels):
            raise IndexError("invalid channel index")

        return channels[id]

    def __init__(self, id: int) -> None:
        # __new__ returns an already-initialized channel from the pool, so
        # the public Channel(id) path must not re-initialize it.
        pass

    @classmethod
    def _allocate(cls, id: int) -> "Channel":
        self = object.__new__(cls)
        self._id = id
        self._track = _sdl3_mixer.Track(MixerInternals.mixer)
        self._track.set_stopped_callback(self._stopped_callback)
        self._sound = None
        self._queued_sound = None
        self._start_time = 0  # Used for mixer.find_channel
        self._end_event = 0
        return self

    def _stopped_callback(self, _: _sdl3_mixer.Track, __: None) -> None:
        if self._end_event and pygame.display.get_init():
            pygame.event.post(pygame.Event(self._end_event, {}))

        # Be sure to set the sound back to None when it's done playing!
        self._sound = None

        if self._queued_sound is not None:
            self.play(self._queued_sound)

    @property
    def id(self) -> int:
        return self._id

    def play(
        self,
        sound: Sound,
        loops: int = 0,
        maxtime: int = -1,
        fade_ms: int = -1,
    ) -> None:
        if self._sound is not None:
            self._track.remove_tag(self._sound._tag)

        self._sound = sound
        self._queued_sound = None
        self._track.set_audio(sound._audio)
        self._track.add_tag(sound._tag)
        self._track.play(loops=loops, max_ms=maxtime, fadein_ms=fade_ms)
        self._start_time = pygame.time.get_ticks()

    def stop(self) -> None:
        self._track.stop()

    def pause(self) -> None:
        self._track.pause()

    def unpause(self) -> None:
        self._track.resume()

    def fadeout(self, time: int, /) -> None:
        self._track.stop(fade_out_frames=self._track.ms_to_frames(time))

    def queue(self, sound: Sound, /) -> None:
        if not isinstance(sound, Sound):
            raise TypeError("The argument must be an instance of Sound")

        if not self.get_busy():
            self.play(sound)
        else:
            self._queued_sound = sound

    def set_source_location(self, angle: float, distance: float, /) -> None:
        distance = round(distance)
        if distance < 0.0 or distance >= 256.0:
            raise ValueError("distance out of range, expected (0, 255)")

        x = math.sin(angle) * distance
        z = math.cos(angle) * distance
        self._track.set_3d_position((x, 0, z))

    def set_volume(self, arg1: float, arg2: float | None = -1.0, /):
        if arg2 == -1.0:
            self._track.gain = arg1
            return

        if arg2 is None:
            arg2 = arg1

        self._track.set_stereo(arg1, arg2)

    def get_volume(self) -> float:
        return self._track.gain

    def get_busy(self) -> bool:
        return self._track.playing

    def get_sound(self) -> Sound | None:
        return self._sound

    def get_queue(self) -> Sound | None:
        return self._queued_sound

    def set_endevent(self, type: int = 0, /) -> None:
        if not isinstance(type, int):
            raise TypeError(
                f"'{type(id).__name__}'object cannot be interpreted as an integer"
            )

        self._end_event = type

    def get_endevent(self) -> int:
        return self._end_event


SoundType = Sound
ChannelType = Channel


class MusicImplementation:
    def __init__(self) -> None:
        self._audio: _sdl3_mixer.Audio | None = None
        self._track: _sdl3_mixer.Track | None = None

        self._queued_audio: _sdl3_mixer.Audio | None = None
        self._queued_loops = 0

        self._end_event = 0

    def _init(self) -> None:
        self._track = _sdl3_mixer.Track(MixerInternals.mixer)
        self._track.set_stopped_callback(self._stopped_callback)

    def _quit(self) -> None:
        self._audio: _sdl3_mixer.Audio | None = None
        self._track: _sdl3_mixer.Track | None = None

        self._queued_audio: _sdl3_mixer.Audio | None = None
        self._queued_loops = 0

        self._end_event = 0

    def _stopped_callback(self, _: _sdl3_mixer.Track, __: None) -> None:
        if self._end_event and pygame.display.get_init():
            pygame.event.post(pygame.Event(self._end_event, {}))

        if self._queued_audio is not None:
            self._audio = self._queued_audio
            self._queued_audio = None

            self._track.set_audio(self._audio)
            self._track.play(loops=self._queued_loops)

            self._queued_loops = 0

    def load(self, filename, namehint: str = "") -> None:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        self._audio = _sdl3_mixer.Audio(
            filename, predecode=False, preferred_mixer=MixerInternals.mixer
        )
        self._track.set_audio(self._audio)

        # Reset old queue state on fresh load
        self._queued_audio = None
        self._queued_loops = 0

    def unload(self) -> None:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        self._audio = None
        self._queued_audio = None
        self._queued_loops = 0
        self._track.set_audio(None)

    def play(self, loops: int = 0, start: float = 0.0, fade_ms: int = 0) -> None:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        self._track.play(
            loops=loops, start_ms=round(start * 1000), fadein_ms=round(fade_ms)
        )

    def rewind(self) -> None:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        self._track.play()

    def stop(self) -> None:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        self._track.stop()

    def pause(self) -> None:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        self._track.pause()

    def unpause(self) -> None:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        self._track.resume()

    def fadeout(self, time: int, /) -> None:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        self._track.stop(fade_out_frames=self._track.ms_to_frames(round(time)))

    def set_volume(self, volume: float, /) -> None:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        self._track.gain = volume

    def get_volume(self) -> float:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        return self._track.gain

    def get_busy(self) -> bool:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        return self._track.playing

    def set_pos(self, pos: float, /) -> None:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        self._track.set_playback_position(self._track.ms_to_frames(round(pos * 1000)))

    def get_pos(self) -> int:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        if self._audio is None:
            return -1

        # TODO: this implementation is not faithful to the original
        # See https://github.com/pygame-community/pygame-ce/pull/3843#discussion_r3554684908
        return self._track.frames_to_ms(self._track.get_playback_position())

    def queue(self, filename: FileLike, namehint: str = "", loops: int = 0) -> None:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        self._queued_audio = _sdl3_mixer.Audio(
            filename, predecode=False, preferred_mixer=MixerInternals.mixer
        )
        self._queued_loops = loops

    def set_endevent(self, event_type: int, /) -> None:
        if not isinstance(type, int):
            raise TypeError(
                f"'{type(id).__name__}'object cannot be interpreted as an integer"
            )

        self._end_event = event_type

    def get_endevent(self) -> int:
        return self._end_event

    def get_metadata(
        self, filename: FileLike | None = None, namehint: str = ""
    ) -> dict:
        if self._track is None:
            raise pygame.error("mixer not initialized")

        if filename is None:
            audio = self._audio
            if audio is None:
                raise pygame.error("music not loaded")
        else:
            audio = _sdl3_mixer.Audio(filename)

        metadata = audio.get_metadata()

        return {
            "title": metadata.title or "",
            "album": metadata.album or "",
            "artist": metadata.artist or "",
            "copyright": metadata.copyright or "",
        }


music = MusicImplementation()
