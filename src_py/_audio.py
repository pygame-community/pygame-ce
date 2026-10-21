"""Pygame module for low level audio control."""

import weakref

import pygame.base
from pygame import _base_audio  # pylint: disable=no-name-in-module
from pygame.typing import FileLike

# TODO: top level details docstring describing the whole flow and mojo
# TODO: Tests
# TODO: make it safe to quit the audio subsystem (e.g. what happens with
# the objects that are now invalid in SDL's eyes.)
# TODO: needs something for SDL_GetAudioDeviceFormat
# TODO: needs something for SDL_OpenAudioDeviceStream
# TODO: ability to create an audiostream with NULL src or dst spec
# TODO: do we need the ability to bind/unbind multiple streams at once
# atomically like SDL_BindAudioStreams


class AudioFormat:
    """Pygame constant object representing the format of audio samples.

    Pygame-ce has the following built in audio formats:
    ::

        pygame._audio.UNKNOWN    # Unknown audio format.
        pygame._audio.U8         # Unsigned 8 bit samples.
        pygame._audio.S8         # Signed 8 bit samples.
        pygame._audio.S16        # Signed 16 bit samples (system-endian).
        pygame._audio.S16LE      # Signed 16 bit samples (little-endian).
        pygame._audio.S16BE      # Signed 16 bit samples (big-endian).
        pygame._audio.S32        # Signed 32 bit samples (system-endian).
        pygame._audio.S32LE      # Signed 32 bit samples (little-endian).
        pygame._audio.S32BE      # Signed 32 bit samples (big-endian).
        pygame._audio.F32        # Floating point 32 bit samples (system-endian).
        pygame._audio.F32LE      # Floating point 32 bit samples (little-endian).
        pygame._audio.F32BE      # Floating point 32 bit samples (big-endian).

    It is not possible to create custom formats. Unlike in pygame-ce 2, unsigned
    16 bit samples are not supported.
    """

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
        """Size of the format, in bits. For example S16 -> 16 bits."""

        return self._value & AudioFormat._MASK_BITSIZE

    @property
    def bytesize(self) -> int:
        """Size of the format, in bytes. For example S16 -> 2 bytes."""

        return self.bitsize // 8

    @property
    def is_float(self) -> bool:
        """Whether the format represents floating point samples (e.g. F32)."""

        return bool(self._value & AudioFormat._MASK_FLOAT)

    @property
    def is_int(self) -> bool:
        """Whether the format represents integer samples (e.g. S16)."""

        return not self.is_float

    @property
    def is_big_endian(self) -> bool:
        """Whether the samples are stored in big-endian byteorder (e.g. S16BE)."""

        return bool(self._value & AudioFormat._MASK_BIG_ENDIAN)

    @property
    def is_little_endian(self) -> bool:
        """Whether the samples are stored in little-endian byteorder (e.g. S16LE)."""

        return not self.is_big_endian

    @property
    def is_signed(self) -> bool:
        """Whether the format uses signed samples (e.g. S16)."""

        return bool(self._value & AudioFormat._MASK_SIGNED)

    @property
    def is_unsigned(self) -> bool:
        """Whether the format uses unsigned samples (e.g. U8)."""

        return not self.is_signed

    @property
    def name(self) -> str:
        """The name of the format."""

        return self._name

    @property
    def silence_value(self) -> bytes:
        """Returns a single byte bytes object equivalent to one sample of silence."""

        return _base_audio.get_silence_value_for_format(self._value)

    # TODO maybe unnecessary?
    def __index__(self) -> int:
        """Returns the actual constant value needed for calls to SDL"""
        return self._value

    def __repr__(self) -> str:
        return f"pygame.audio.{self._name}"


class AudioSpec:
    """Pygame object specifying layout of raw audio data.

    Contains the per-sample format (:class:`AudioFormat`), the number of channels
    (1=mono, 2=stereo, etc.), as well as the frequency.

    AudioSpec's are immutable, like tuples. Once created, the format, channels,
    and frequency are not able to be changed.
    """

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
        """The specified AudioFormat."""

        return self._format

    @property
    def channels(self) -> int:
        """The specified number of channels."""

        return self._channels

    @property
    def frequency(self) -> int:
        """The specified frequency."""

        return self._frequency

    @property
    def framesize(self) -> int:
        """The size of each frame of audio.

        For example, S16 stereo data (2 channels * 2 bytes per sample) would
        be 4 bytes per frame.
        """

        return self._format.bytesize * self.channels

    def __repr__(self) -> str:
        return (
            self.__class__.__name__
            + f"({self._format}, {self._channels}, {self._frequency})"
        )


class AudioDevice:
    """Pygame object representing an audio device connected to the system.

    Each AudioDevice is either a playback device (e.g. a speaker), or a
    recording device (e.g. a microphone). This class represents the device
    itself; to play audio one must :meth:`open()` the device to get a
    :class:`LogicalAudioDevice`.

    To find the system's AudioDevice's, call :func:`pygame._audio.get_playback_devices()`
    or :func:`pygame._audio.get_recording_devices()`.

    For most use cases, it is best to use :attr:`pygame._audio.DEFAULT_PLAYBACK_DEVICE`
    or :attr:`pygame._audio.DEFAULT_RECORDING_DEVICE`.
    """

    # For folks reading the SDL docs, this class represents all
    # "physical audio devices."

    # def __repr__(self) -> str:
    #    return f"AudioDevice with name {self.name}"

    def open(self, spec: AudioSpec | None = None) -> "LogicalAudioDevice":
        """Get an independent LogicalAudioDevice that can be bound to an AudioStream.

        Optionally, an :class:`AudioSpec` can be provided as a hint for the
        layout of audio data the program would like to use, but there is no
        guarantee the device will use that directly. :class:`AudioStream`
        will manage any needed spec conversions.

        For recording devices, :class:`LogicalAudioDevice` will push data to
        bound stream(s). For playback devices, :class:`LogicalAudioDevice` will
        pull data from bound stream(s).

        An AudioDevice can be opened multiple times, the
        :class:`LogicalAudioDevice`'s will not conflict with each other.
        """

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
        """Whether the AudioDevice is a playback device (e.g. a speaker) or not."""

        return _base_audio.is_audio_device_playback(self._state)

    @property
    def name(self) -> str:
        """The human-readable name of the AudioDevice.

        .. note::
            Be aware that the name of the default recording and playback
            devices will not be stable, since the underlying device can change.
        """

        return _base_audio.get_audio_device_name(self._state)

    @property
    def channel_map(self) -> list[int] | None:
        """Returns the channel map applied to the AudioDevice, or None.

        If there is remapping applied on the audio device, this will return
        a channel map.
        """

        return _base_audio.get_audio_device_channel_map(self._state)


class LogicalAudioDevice(AudioDevice):
    """Pygame object representing a handle to an audio device.

    LogicalAudioDevices are created by calling :func:`AudioDevice.open()`.
    For example, ``device = pygame._audio.DEFAULT_PLAYBACK_DEVICE.open()``.

    LogicalAudioDevices are used to bind to one or multiple :class:`AudioStream`
    instances.

    This class is a subclass of :class:`AudioDevice`, AudioDevice methods
    are also valid to use here.
    """

    def pause(self) -> None:
        """Stops all audio processing through this logical device.

        Any bound AudioStreams will not progress. Pausing one device does not
        prevent other unpaused devices from running.

        LogicalAudioDevices start un-paused.
        """

        _base_audio.pause_audio_device(self._state)

    def resume(self) -> None:
        """Resumes all audio processing through this logical device."""

        _base_audio.resume_audio_device(self._state)

    @property
    def paused(self) -> bool:
        """Whether the logical device is paused or not."""

        return _base_audio.audio_device_paused(self._state)

    @property
    def gain(self) -> float:
        """Gets or sets the gain (the volume).

        Larger gain = louder, gain of zero means silence. The default gain is
        1.0 (no change in output).
        """

        return _base_audio.get_audio_device_gain(self._state)

    @gain.setter
    def gain(self, value: float) -> None:
        if value < 0:
            raise ValueError("Gain must be >= 0.")
        _base_audio.set_audio_device_gain(self._state, value)


class AudioStream:
    """Pygame object representing an audio input/output stream.

    AudioStreams are a versatile audio conversion interface. They take in a
    src_spec (source AudioSpec) and a dst_spec (destination AudioSpec).
    Raw data can be added with :meth:`put_data`, and the converted data
    can be retrieved with :meth:`get_data`.

    AudioStreams can be bound to a playback or recording
    :class:`LogicalAudioDevice`. When bound to a playback device, pygame-ce
    takes over the get_data side, and when bound to a recording device,
    pygame-ce takes over the put_data side. For example, when hooked up to a
    recording device, raw audio data will be automatically put into the stream,
    and the converted audio can be retrieved as it becomes available by get_data.

    When an AudioStream is bound, the src_spec or dst_spec may be changed to
    match the bound device (for recording devices and playback devices respectively).
    In addition, the src_spec and dst_spec may not be changed when their
    respective side of the stream is bound to a logical device.

    - It can handle resampling data in chunks without generating artifacts,
      when it doesn't have the complete buffer available.
    - It can handle incoming data in any variable size.
    - It can handle input/output format changes on the fly.
    - It can remap audio channels between inputs and outputs.
    - You push data as you have it, and pull it when you need it
    - It can also function as a basic audio data queue even if you just have
      sound that needs to pass from one place to another.
    - (TODO) You can hook callbacks up to them when more data is added or requested,
      to manage data on-the-fly.
    """

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
        """Connect a stream to a LogicalAudioDevice for recording/playback.

        For a playback device, data for all streams on the device will be
        mixed together and fed to the device. For a recording device, a copy
        of recorded data will be provided to each stream on the device.

        If the stream is already bound, this will raise :exc:`pygame.error`.
        The stream must first be explicitly unbound via the :meth:`unbind()`
        method.

        Binding a stream to a device will set its output format for playback
        devices, and its input format for recording devices, so they match the
        device's settings. The caller is welcome to change the other end of the
        stream's format at any time with :attr:`dst_spec` or :attr:`src_spec`.
        """

        # Not yet relevant bit from SDL docs:
        # If the other end of the stream's format has never been set (the audio stream was created
        # with a NULL audio spec), this function will set it to match the device
        # end's format.

        if not isinstance(device, LogicalAudioDevice):
            raise TypeError(
                f"AudioStream bind argument must be LogicalAudioDevice, received {type(device)}"
            )

        _base_audio.bind_audio_stream(device._state, self._state)
        self._device = device

    def unbind(self) -> None:
        """Disconnect a stream from a LogicalAudioDevice.

        If the stream is not bound, this does nothing.
        """

        _base_audio.unbind_audio_stream(self._state)
        self._device = None

    def clear(self) -> None:
        """Clear any pending data in the stream.

        This drops any queued data, so there will be nothing to read from
        the stream until more is added.
        """

        _base_audio.clear_audio_stream(self._state)

    def flush(self) -> None:
        """Tell the stream to convert everything in its buffer.

        This tells the stream that you're done sending data, and anything
        buffered should be converted/resampled and made available immediately.

        It is legal to add more data to a stream after flushing, but there may
        be audio gaps in the output. Generally this is intended to signal the
        end of input, so the complete output becomes available.
        """

        _base_audio.flush_audio_stream(self._state)

    @property
    def num_available_bytes(self) -> int:
        """Get the number of converted/resampled bytes available.

        The stream may be buffering data behind the scenes until it has enough
        to resample correctly, so this number might be lower than what you
        expect, or even be zero. Add more data or :meth:`flush()` the stream
        if you need the data now.

        If the stream has so much data that it would overflow a C int, the
        return value is clamped to a maximum value, but no queued data is lost;
        if there are gigabytes of data queued, the app might need to read some
        of it with :meth:`get_data()` before this value is no longer clamped.
        """

        return _base_audio.get_audio_stream_available(self._state)

    @property
    def num_queued_bytes(self) -> int:
        """Get the number of bytes currently queued.

        This is the number of bytes put into the stream as input, not the
        number that can be retrieved as output.

        If the stream has so much data that it would overflow a C int, the
        return value is clamped to a maximum value, but no queued data is lost;
        if there are gigabytes of data queued, the app might need to read some
        of it with :meth:`get_data()` before this value is no longer clamped.

        .. note::
            AudioStreams can change their input format at any time, even if
            there is still data queued in a different format, so the returned
            byte count will not necessarily match the number of sample frames
            available.
        """

        return _base_audio.get_audio_stream_queued(self._state)

    def get_data(self, size: int) -> bytes:
        """Get up to "size" bytes of converted/resampled data from the AudioStream.

        Any necessary conversion and resampling is done during this call, into
        the :attr:`dst_spec` AudioSpec.

        .. seealso:: :meth:`put_data()`
        """

        return _base_audio.get_audio_stream_data(self._state, size)

    # TODO: replace bytes | bytearray | memoryview with collections.abc.Buffer
    # when we support only 3.12 and up.
    def put_data(self, data: bytes | bytearray | memoryview) -> None:
        """Add raw data to the stream.

        The data can be a bytes object, a bytearray, a memoryview, anything
        that supports the buffer protocol. The data must match the details
        (format/channels/frequency) of the :attr:`src_spec` AudioSpec.

        This method copies the data into the stream, but the actual conversion
        to the destination AudioSpec is done in :meth:`get_data()`.
        """

        _base_audio.put_audio_stream_data(self._state, data)

    def pause_device(self) -> None:
        """Pauses the stream's bound LogicalAudioDevice.

        If there is no bound device, this will raise :exc:`pygame.error`.
        """

        _base_audio.pause_audio_stream_device(self._state)

    def resume_device(self) -> None:
        """Resumes the stream's bound LogicalAudioDevice.

        If there is no bound device, this will raise :exc:`pygame.error`.
        """

        _base_audio.resume_audio_stream_device(self._state)

    @property
    def device_paused(self) -> bool:
        """Gets whether the stream's bound LogicalAudioDevice is paused.

        If there is no bound device, this will return ``False``.
        """

        return _base_audio.audio_stream_device_paused(self._state)

    @property
    def device(self) -> LogicalAudioDevice | None:
        """Gets the stream's bound LogicalAudioDevice (or None if not bound)."""

        return self._device

    @property
    def src_spec(self) -> AudioSpec:
        """Gets or sets the source (input) AudioSpec.

        This specifies the data layout for the raw data in :meth:`put_data()`.

        If this stream is bound to a recording logical audio device, the src_spec
        cannot be changed. This will raise a :exc:`pygame.error`.
        """
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
        """Gets or sets the destination (output) AudioSpec.

        This specifies the data layout for the converted data in :meth:`get_data()`.

        If this stream is bound to a playback logical audio device, the dst_spec
        cannot be changed. This will raise a :exc:`pygame.error`.
        """

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
        """Gets or sets the gain (the volume).

        Larger gain = louder, gain of zero means silence. The default gain is
        1.0 (no change in output).
        """

        return _base_audio.get_audio_stream_gain(self._state)

    @gain.setter
    def gain(self, value: float) -> None:
        if value < 0:
            raise ValueError("Gain must be >= 0.")

        _base_audio.set_audio_stream_gain(self._state, value)

    @property
    def frequency_ratio(self) -> float:
        """Gets or sets the frequency ratio.

        The frequency ratio is used to adjust the rate at which input data is
        consumed. Changing this effectively modifies the speed and pitch of
        the audio. A value less than 1.0 will play the audio slower, and at a
        lower pitch. 1.0 means play at normal speed.

        This is applied during :meth:`get_data()` and can be continuously
        changed to create various effects.
        """

        return _base_audio.get_audio_stream_frequency_ratio(self._state)

    @frequency_ratio.setter
    def frequency_ratio(self, value: float) -> None:
        if value <= 0 or value > 10:
            raise ValueError(
                "Frequency ratio must be between 0 and 10. (0 < ratio <= 10)"
            )

        _base_audio.set_audio_stream_frequency_ratio(self._state, value)

    def lock(self) -> None:
        # TODO: document. Seems only relevant during callbacks, which aren't implemented yet.

        _base_audio.lock_audio_stream(self._state)

    def unlock(self) -> None:
        # TODO: document. Seems only relevant during callbacks, which aren't implemented yet.

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
    """Initialize the audio subsystem."""

    _base_audio.init()


# See TODO above, this is currently not safe to offer
# def quit() -> None:
#    _base_audio.quit()


def get_init() -> bool:
    """Returns whether the audio subsystem is initialized."""

    return _base_audio.get_init()


def get_current_driver() -> str:
    """Get the name of the currently used audio interface.

    .. seealso:: :func:`pygame._audio.get_drivers()`
    """

    return _base_audio.get_current_driver()


def get_drivers() -> list[str]:
    """Get a list of available audio interfaces.

    These are the interfaces with support compiled in, they are not guaranteed
    to be functional.
    """

    return _base_audio.get_drivers()


def get_playback_devices() -> list[AudioDevice]:
    """Get a list of available playback devices (e.g. speakers).

    .. seealso:: :func:`pygame._audio.get_recording_devices()`
    """

    return [
        _internals.create_audio_device(dev_state)
        for dev_state in _base_audio.get_playback_device_states()
    ]


def get_recording_devices() -> list[AudioDevice]:
    """Get a list of available recording devices (e.g. microphones).

    .. seealso:: :func:`pygame._audio.get_playback_devices()`
    """

    return [
        _internals.create_audio_device(dev_state)
        for dev_state in _base_audio.get_recording_device_states()
    ]


def load_wav(file: FileLike) -> tuple[AudioSpec, bytes]:
    """Takes a source of WAV data and returns an AudioSpec and raw bytes.

    Accepts a path or a file-like object with WAV audio data, returns an
    :class:`AudioSpec` and a bytes object with the samples laid out per the
    AudioSpec.

    Supported formats are RIFF WAVE files with the formats PCM (8, 16, 24,
    and 32 bits), IEEE Float (32 bits), Microsoft ADPCM and IMA ADPCM (4 bits),
    and A-law and mu-law (8 bits). Other formats are currently unsupported
    and cause an error.
    """

    audio_bytes, format_num, channels, frequency = _base_audio.load_wav(file)
    return (
        _internals.audio_spec_from_ints(format_num, channels, frequency),
        audio_bytes,
    )


DEFAULT_PLAYBACK_DEVICE = _internals.create_audio_device(
    _base_audio.get_default_playback_device_state()
)
"""Default playback AudioDevice.

Rather than representing a specific speaker, this represents the default
speaker, which may change during the program if playback devices are
added/removed, or the user changes the default.

If the underlying physical device changes, audio playing through this
will seamlessly change over to the new default device.
"""

DEFAULT_RECORDING_DEVICE = _internals.create_audio_device(
    _base_audio.get_default_recording_device_state()
)
"""Default recording AudioDevice.

Rather than representing a specific microphone, this represents the default
microphone, which may change during the program if recording devices are
added/removed, or the user changes the default.

If the underlying physical device changes, audio recording through this
will seamlessly change over to the new default device.
"""

# Don't re-export names if it can be helped
del weakref, FileLike, AudioInternals
