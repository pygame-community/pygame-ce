import dataclasses
import weakref

import pygame
from pygame import _audio as audio, _sdl3_mixer_c  # pylint: disable=no-name-in-module

init = _sdl3_mixer_c.init
get_sdl_mixer_version = _sdl3_mixer_c.get_sdl_mixer_version


# Pure Python version of MIX_MSToFrames, since it's so straightforward.
def ms_to_frames(sample_rate: int, ms: int) -> int:
    if sample_rate <= 0:
        raise ValueError("Sample rate must be greater than zero.")
    if ms < 0:
        raise ValueError("MS must be non-negative.")

    return int(ms / 1000 * sample_rate)


# Pure Python version of MIX_FramesToMS, since it's so straightforward.
def frames_to_ms(sample_rate: int, frames: int) -> int:
    if sample_rate <= 0:
        raise ValueError("Sample rate must be greater than zero.")
    if frames < 0:
        raise ValueError("Frames must be non-negative.")

    return int(frames / sample_rate * 1000)


get_decoders = _sdl3_mixer_c.get_decoders


class _MixerInternals:
    def __init__(self) -> None:
        # Used for object cleanup when quit() is called.
        self._mixers = weakref.WeakSet()
        self._tracks = weakref.WeakSet()
        self._audios = weakref.WeakSet()
        self._audio_decoders = weakref.WeakSet()

    def add_mixer_ref(self, mixer: "Mixer") -> None:
        self._mixers.add(mixer)

    def add_track_ref(self, track: "Track") -> None:
        self._tracks.add(track)

    def add_audio_ref(self, audio_obj: "Audio") -> None:
        self._audios.add(audio_obj)

    def add_audio_decoder_ref(self, decoder: "AudioDecoder") -> None:
        self._audio_decoders.add(decoder)

    def destroy_all_dynamic_objects(self) -> None:
        """Before quitting the mixer subsystem, we need to invalidate our
        references to it so that objects created before and used after do
        not segfault or violate any SDL_mixer assumptions.

        Mirrors AudioInternals.destroy_all_dynamic_objects in _audio.py.

        Tracks must be destroyed before their owning Mixer: MIX_DestroyMixer
        destroys all of its own tracks internally (and, unlike MIX_Audio,
        tracks are not reference-counted), so destroying a Track after its
        Mixer is already gone would double free it.
        """

        for track in self._tracks:
            track._destroy()

        for audio_obj in self._audios:
            audio_obj._destroy()

        for decoder in self._audio_decoders:
            decoder._destroy()

        for mixer in self._mixers:
            mixer._destroy()

        self._tracks.clear()
        self._audios.clear()
        self._audio_decoders.clear()
        self._mixers.clear()


_internals = _MixerInternals()


def quit() -> None:
    """Quit the mixer subsystem. This invalidates all mixer objects."""

    _internals.destroy_all_dynamic_objects()
    _sdl3_mixer_c.quit()


class Mixer(_sdl3_mixer_c.Mixer):
    def __init__(
        self,
        device: audio.AudioDevice = audio.DEFAULT_PLAYBACK_DEVICE,
        spec: audio.AudioSpec | None = None,
    ) -> None:
        if self._valid:
            raise RuntimeError("Object of type Mixer cannot be reinitialized")

        if not isinstance(device, audio.AudioDevice):
            raise TypeError(
                "Mixer init 'device' argument must be an AudioDevice, "
                f"received {type(device)}"
            )
        device._check_valid()

        if spec is None:
            _sdl3_mixer_c.Mixer.__init__(self, device._state, None)
        elif isinstance(spec, audio.AudioSpec):
            _sdl3_mixer_c.Mixer.__init__(
                self, device._state, (spec.format, spec.channels, spec.frequency)
            )
        else:
            raise TypeError(
                "Mixer init 'spec' argument must be an AudioSpec "
                f"or None, received {type(spec)}"
            )

        _internals.add_mixer_ref(self)

    @property
    def spec(self) -> audio.AudioSpec:
        return audio._internals.audio_spec_from_ints(
            *_sdl3_mixer_c.Mixer._get_spec(self)
        )


@dataclasses.dataclass(frozen=True)
class AudioMetadata:
    title: str | None
    artist: str | None
    album: str | None
    copyright: str | None
    track_num: int | None
    total_tracks: int | None


class Audio(_sdl3_mixer_c.Audio):
    def __init__(
        self,
        file,
        predecode: bool = False,
        preferred_mixer: Mixer | None = None,
    ) -> None:
        _sdl3_mixer_c.Audio.__init__(self, file, predecode, preferred_mixer)
        _internals.add_audio_ref(self)

    @classmethod
    def from_raw(
        cls, buffer, spec: audio.AudioSpec, preferred_mixer: Mixer | None = None
    ):
        if not isinstance(spec, audio.AudioSpec):
            raise TypeError(
                f"Audio 'spec' argument must be an AudioSpec, received {type(spec)}"
            )

        result = super().from_raw(
            buffer, (spec.format, spec.channels, spec.frequency), preferred_mixer
        )
        _internals.add_audio_ref(result)
        return result

    @classmethod
    def from_sine_wave(
        cls,
        hz: int,
        amplitude: float,
        ms: int = -1,
        preferred_mixer: Mixer | None = None,
    ):
        result = super().from_sine_wave(hz, amplitude, ms, preferred_mixer)
        _internals.add_audio_ref(result)
        return result

    @property
    def spec(self) -> audio.AudioSpec:
        return audio._internals.audio_spec_from_ints(
            *_sdl3_mixer_c.Audio._get_spec(self)
        )

    def get_metadata(self) -> AudioMetadata:
        metadata = _sdl3_mixer_c.Audio.get_metadata(self)
        return AudioMetadata(
            title=metadata["title"],
            artist=metadata["artist"],
            album=metadata["album"],
            copyright=metadata["copyright"],
            track_num=metadata["track_num"],
            total_tracks=metadata["total_tracks"],
        )


class Track(_sdl3_mixer_c.Track):
    def __init__(self, mixer: Mixer) -> None:
        if self._valid:
            raise RuntimeError("Object of type Track cannot be reinitialized")

        if not isinstance(mixer, Mixer):
            raise TypeError(
                f"Track 'mixer' argument must be a Mixer, received {type(mixer)}"
            )

        _sdl3_mixer_c.Track.__init__(self, mixer)
        _internals.add_track_ref(self)

    def set_audiostream(self, audiostream: audio.AudioStream | None) -> None:
        if not self._valid:
            raise pygame.error("Dead Track, the track was destroyed")

        if isinstance(audiostream, audio.AudioStream):
            audiostream._check_valid()
            _sdl3_mixer_c.Track.set_audiostream(self, audiostream)
        elif audiostream is None:
            _sdl3_mixer_c.Track.set_audiostream(self, None)
        else:
            raise TypeError(
                "audiostream argument must be an AudioStream or None, "
                f"received {type(audiostream)}"
            )


class AudioDecoder(_sdl3_mixer_c.AudioDecoder):
    def __init__(self, file) -> None:
        _sdl3_mixer_c.AudioDecoder.__init__(self, file)
        _internals.add_audio_decoder_ref(self)

    @property
    def spec(self) -> audio.AudioSpec:
        return audio._internals.audio_spec_from_ints(
            *_sdl3_mixer_c.AudioDecoder._get_spec(self)
        )

    def decode(self, spec: audio.AudioSpec, size: int | None = None) -> bytes:
        if not self._valid:
            raise pygame.error("Dead AudioDecoder, the audio decoder was destroyed")

        if not isinstance(spec, audio.AudioSpec):
            raise TypeError(
                f"decode 'spec' argument must be an AudioSpec, received {type(spec)}"
            )

        return _sdl3_mixer_c.AudioDecoder.decode(
            self, (spec.format, spec.channels, spec.frequency), size
        )
