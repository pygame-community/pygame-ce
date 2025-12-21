import weakref

import pygame.base
from pygame import _base_audio  # pylint: disable=no-name-in-module
from pygame.typing import FileLike

# TODO: Docs
# TODO: Tests
# TODO: make it safe to quit the audio subsystem (e.g. what happens with
# the objects that are now invalid in SDL's eyes.)


class AudioFormat:
    # AudioFormat details pulled from SDL_audio.h header files
    # These details are stable for the lifetime of SDL3, as programs built
    # on one release will be able to run on newer releases.
    _MASK_BITSIZE = 0xFF
    _MASK_FLOAT = 1 << 8
    _MASK_BIG_ENDIAN = 1 << 12
    _MASK_SIGNED = 1 << 15

    # These objects are constructed externally, putting these here
    # to annotate the attributes that are populated.
    _value: int
    _name: str

    @property
    def bitsize(self) -> int:
        return self._value & AudioFormat._MASK_BITSIZE

    @property
    def bytesize(self) -> int:
        return self.bitsize // 8

    @property
    def is_float(self) -> bool:
        return bool(self._value & AudioFormat._MASK_FLOAT)

    @property
    def is_int(self) -> bool:
        return not self.is_float

    @property
    def is_big_endian(self) -> bool:
        return bool(self._value & AudioFormat._MASK_BIG_ENDIAN)

    @property
    def is_little_endian(self) -> bool:
        return not self.is_big_endian

    @property
    def is_signed(self) -> bool:
        return bool(self._value & AudioFormat._MASK_SIGNED)

    @property
    def is_unsigned(self) -> bool:
        return not self.is_signed

    @property
    def name(self) -> str:
        return self._name

    @property
    def silence_value(self) -> bytes:
        return _base_audio.get_silence_value_for_format(self._value)

    # TODO maybe unnecessary?
    def __index__(self) -> int:
        """Returns the actual constant value needed for calls to SDL"""
        return self._value

    def __repr__(self) -> str:
        return f"pygame.audio.{self._name}"


class AudioSpec:
    def __init__(self, format: AudioFormat, channels: int, frequency: int) -> None:
        if not isinstance(format, AudioFormat):
            raise TypeError(
                f"AudioSpec format must be an AudioFormat, received {type(format)}"
            )

        if channels < 1 or channels > 8:
            raise ValueError("Invalid channel count, should be between 1 and 8.")

        # AudioSpecs are immutable so that they can be owned by other things
        # like AudioStreams without worrying about what happens if someone
        # changes the spec externally.
        self._format = format
        self._channels = channels
        self._frequency = frequency

    @property
    def format(self) -> AudioFormat:
        return self._format

    @property
    def channels(self) -> int:
        return self._channels

    @property
    def frequency(self) -> int:
        return self._frequency

    @property
    def framesize(self) -> int:
        return self._format.bytesize * self.channels

    def __repr__(self) -> str:
        return (
            self.__class__.__name__
            + f"({self._format}, {self._channels}, {self._frequency})"
        )


class AudioDevice:
    # def __repr__(self) -> str:
    #    return f"AudioDevice with name {self.name}"

    def open(self, spec: AudioSpec | None = None) -> "LogicalAudioDevice":
        if spec is None:
            dev_state = _base_audio.open_audio_device(self._state)
        elif isinstance(spec, AudioSpec):
            dev_state = _base_audio.open_audio_device(
                self._state, spec.format, spec.channels, spec.frequency
            )
        else:
            raise TypeError(
                "AudioDevice open 'spec' argument must be an AudioSpec "
                f"or None, received {type(spec)}"
            )

        device = object.__new__(LogicalAudioDevice)
        device._state = dev_state
        return device

    @property
    def is_playback(self) -> bool:
        return _base_audio.is_audio_device_playback(self._state)

    # TODO: this doesn't work for the default device ids...
    # https://github.com/libsdl-org/SDL/issues/14615
    @property
    def name(self) -> str:
        return _base_audio.get_audio_device_name(self._state)

    @property
    def channel_map(self) -> list[int] | None:
        return _base_audio.get_audio_device_channel_map(self._state)


class LogicalAudioDevice(AudioDevice):
    def pause(self) -> None:
        _base_audio.pause_audio_device(self._state)

    def resume(self) -> None:
        _base_audio.resume_audio_device(self._state)

    @property
    def paused(self) -> bool:
        return _base_audio.audio_device_paused(self._state)

    @property
    def gain(self) -> float:
        return _base_audio.get_audio_device_gain(self._state)

    @gain.setter
    def gain(self, value: float) -> None:
        if value < 0:
            raise ValueError("Gain must be >= 0.")
        _base_audio.set_audio_device_gain(self._state, value)


class AudioStream:
    def __init__(self, src_spec: AudioSpec, dst_spec: AudioSpec) -> None:
        if not isinstance(src_spec, AudioSpec):
            raise TypeError(
                f"AudioStream src_spec must be an AudioSpec, received {type(src_spec)}"
            )
        if not isinstance(dst_spec, AudioSpec):
            raise TypeError(
                f"AudioStream dst_spec must be an AudioSpec, received {type(dst_spec)}"
            )

        self._state = _base_audio.create_audio_stream(
            src_spec.format,
            src_spec.channels,
            src_spec.frequency,
            dst_spec.format,
            dst_spec.channels,
            dst_spec.frequency,
        )
        self._device: LogicalAudioDevice | None = None

    def bind(self, device: LogicalAudioDevice) -> None:
        if not isinstance(device, LogicalAudioDevice):
            raise TypeError(
                f"AudioStream bind argument must be LogicalAudioDevice, received {type(device)}"
            )

        _base_audio.bind_audio_stream(device._state, self._state)
        self._device = device

    def unbind(self) -> None:
        _base_audio.unbind_audio_stream(self._state)
        self._device = None

    def clear(self) -> None:
        _base_audio.clear_audio_stream(self._state)

    def flush(self) -> None:
        _base_audio.flush_audio_stream(self._state)

    @property
    def num_available_bytes(self) -> int:
        return _base_audio.get_audio_stream_available(self._state)

    @property
    def num_queued_bytes(self) -> int:
        return _base_audio.get_audio_stream_queued(self._state)

    def get_data(self, size: int) -> bytes:
        return _base_audio.get_audio_stream_data(self._state, size)

    # TODO: replace bytes | bytearray | memoryview with collections.abc.Buffer
    # when we support only 3.12 and up.
    def put_data(self, data: bytes | bytearray | memoryview) -> None:
        _base_audio.put_audio_stream_data(self._state, data)

    def pause_device(self) -> None:
        _base_audio.pause_audio_stream_device(self._state)

    def resume_device(self) -> None:
        _base_audio.resume_audio_stream_device(self._state)

    @property
    def device_paused(self) -> bool:
        return _base_audio.audio_stream_device_paused(self._state)

    @property
    def device(self) -> LogicalAudioDevice | None:
        return self._device

    @property
    def src_spec(self) -> AudioSpec:
        return _internals.audio_spec_from_ints(
            *_base_audio.get_audio_stream_format(self._state)[0:3]
        )

    @src_spec.setter
    def src_spec(self, value: AudioSpec) -> None:
        if not isinstance(value, AudioSpec):
            raise TypeError(
                f"AudioStream src_spec must be an AudioSpec, received {type(value)}"
            )

        # If bound to a non-playback device (e.g. recording device), the input
        # spec can't be changed. SDL itself will ignore these changes,
        # but we are erroring to let the users know not to do this.
        if self.device is not None and not self.device.is_playback:
            raise pygame.error(
                "Cannot change stream src spec while bound to a recording device"
            )

        _base_audio.set_audio_stream_format(
            self._state, (value.format, value.channels, value.frequency), None
        )

    @property
    def dst_spec(self) -> AudioSpec:
        # My first impulse here was to store the Python dst_spec AudioSpec
        # object and just return it here. BUT, SDL can change the output
        # format of the stream internally-
        # Only when it gets bound?
        # To guarantee correctness it now pulls it every time, even though
        # that is inefficient.

        return _internals.audio_spec_from_ints(
            *_base_audio.get_audio_stream_format(self._state)[3:6]
        )

    @dst_spec.setter
    def dst_spec(self, value: AudioSpec) -> None:
        if not isinstance(value, AudioSpec):
            raise TypeError(
                f"AudioStream dst_spec must be an AudioSpec, received {type(value)}"
            )

        # If bound to a playback device, the output spec can't be changed.
        # SDL itself will ignore these changes, but we are erroring to let the users
        # know not to do this.
        if self.device is not None and self.device.is_playback:
            raise pygame.error(
                "Cannot change stream dst spec while bound to a playback device"
            )

        _base_audio.set_audio_stream_format(
            self._state, None, (value.format, value.channels, value.frequency)
        )

    @property
    def gain(self) -> float:
        return _base_audio.get_audio_stream_gain(self._state)

    @gain.setter
    def gain(self, value: float) -> None:
        if value < 0:
            raise ValueError("Gain must be >= 0.")

        _base_audio.set_audio_stream_gain(self._state, value)

    @property
    def frequency_ratio(self) -> float:
        return _base_audio.get_audio_stream_frequency_ratio(self._state)

    @frequency_ratio.setter
    def frequency_ratio(self, value: float) -> None:
        if value <= 0 or value > 10:
            raise ValueError(
                "Frequency ratio must be between 0 and 10. (0 < ratio <= 10)"
            )

        _base_audio.set_audio_stream_frequency_ratio(self._state, value)

    def lock(self) -> None:
        _base_audio.lock_audio_stream(self._state)

    def unlock(self) -> None:
        _base_audio.unlock_audio_stream(self._state)

    def __repr__(self) -> str:
        audio_format_ints = _base_audio.get_audio_stream_format(self._state)
        src_spec = _internals.audio_spec_from_ints(*audio_format_ints[0:3])
        dst_spec = _internals.audio_spec_from_ints(*audio_format_ints[3:6])

        return f"<{self.__class__.__name__}({src_spec}, {dst_spec})>"


class AudioInternals:
    def __init__(self) -> None:
        self._int_to_format: dict[int, AudioFormat] = {}
        self._id_to_device = weakref.WeakValueDictionary()

    def create_format(self, name: str, value: int) -> AudioFormat:
        audio_format = object.__new__(AudioFormat)
        audio_format._name = name
        audio_format._value = value
        self._int_to_format[value] = audio_format
        return audio_format

    def audio_spec_from_ints(
        self, format_num: int, channels: int, frequency: int
    ) -> AudioSpec:
        format_inst = self._int_to_format.get(format_num)
        if format_inst is None:
            raise pygame.error(
                f"Unknown audio format value {format_num}. "
                "Please report to the pygame-ce devs."
            )
        return AudioSpec(format_inst, channels, frequency)

    def create_audio_device(self, dev_state) -> AudioDevice:
        # If a Python AudioDevice is already allocated with that id, use it.
        # Otherwise allocate a new AudioDevice and set its state.
        device = self._id_to_device.get(dev_state.id)
        if device is None:
            device = object.__new__(AudioDevice)
            device._state = dev_state
            self._id_to_device[dev_state.id] = device
        return device


_internals = AudioInternals()


UNKNOWN = _internals.create_format("UNKNOWN", 0x0000)
U8 = _internals.create_format("U8", 0x0008)
S8 = _internals.create_format("S8", 0x8008)
S16LE = _internals.create_format("S16LE", 0x8010)
S16BE = _internals.create_format("S16BE", 0x9010)
S32LE = _internals.create_format("S32LE", 0x8020)
S32BE = _internals.create_format("S32BE", 0x9020)
F32LE = _internals.create_format("F32LE", 0x8120)
F32BE = _internals.create_format("F32BE", 0x9120)

if pygame.base.get_sdl_byteorder() == 1234:
    S16 = S16LE
    S32 = S32LE
    F32 = F32LE
else:
    S16 = S16BE
    S32 = S32BE
    F32 = F32BE


def init() -> None:
    _base_audio.init()


# See TODO above, this is currently not safe to offer
# def quit() -> None:
#    _base_audio.quit()


def get_init() -> bool:
    return _base_audio.get_init()


def get_current_driver() -> str:
    return _base_audio.get_current_driver()


def get_drivers() -> list[str]:
    return _base_audio.get_drivers()


def get_playback_devices() -> list[AudioDevice]:
    return [
        _internals.create_audio_device(dev_state)
        for dev_state in _base_audio.get_playback_device_states()
    ]


def get_recording_devices() -> list[AudioDevice]:
    return [
        _internals.create_audio_device(dev_state)
        for dev_state in _base_audio.get_recording_device_states()
    ]


def load_wav(file: FileLike) -> tuple[AudioSpec, bytes]:
    audio_bytes, format_num, channels, frequency = _base_audio.load_wav(file)
    return (
        _internals.audio_spec_from_ints(format_num, channels, frequency),
        audio_bytes,
    )


DEFAULT_PLAYBACK_DEVICE = _internals.create_audio_device(
    _base_audio.get_default_playback_device_state()
)
DEFAULT_RECORDING_DEVICE = _internals.create_audio_device(
    _base_audio.get_default_recording_device_state()
)

# Don't re-export names if it can be helped
del weakref, FileLike, AudioInternals
