import dataclasses

from pygame import _audio as audio, _sdl3_mixer_c

init = _sdl3_mixer_c.init
# quit = _sdl3_mixer_c.quit
get_sdl_mixer_version = _sdl3_mixer_c.get_sdl_mixer_version


# Pure Python version of MIX_MSToFrames, since it's so straightforward.
def ms_to_frames(sample_rate: int, ms: int) -> int:
    if sample_rate <= 0:
        raise ValueError("Sample rate must be greater than zero.")
    if ms < 0:
        raise ValueError("MS must be positive.")

    return int(ms / 1000 * sample_rate)


# Pure Python version of MIX_FramesToMS, since it's so straightforward.
def frames_to_ms(sample_rate: int, frames: int) -> int:
    if sample_rate <= 0:
        raise ValueError("Sample rate must be greater than zero.")
    if frames < 0:
        raise ValueError("Frames must be positive.")

    return int(frames / sample_rate * 1000)


get_decoders = _sdl3_mixer_c.get_decoders


class Mixer(_sdl3_mixer_c.Mixer):
    def __init__(
        self,
        device: audio.AudioDevice = audio.DEFAULT_PLAYBACK_DEVICE,
        spec: audio.AudioSpec | None = None,
    ) -> None:
        if spec is None:
            _sdl3_mixer_c.Mixer.__init__(self, device._state, spec)
        elif isinstance(spec, audio.AudioSpec):
            _sdl3_mixer_c.Mixer.__init__(
                self, device._state, (spec.format, spec.channels, spec.frequency)
            )
        else:
            raise TypeError(
                "Mixer init 'spec' argument must be an AudioSpec "
                f"or None, received {type(spec)}"
            )

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
        if not isinstance(mixer, Mixer):
            raise TypeError(
                f"Track 'mixer' argument must be a Mixer, received {type(mixer)}"
            )

        _sdl3_mixer_c.Track.__init__(self, mixer)

    def set_audiostream(self, audiostream: audio.AudioStream | None) -> None:
        if isinstance(audiostream, audio.AudioStream):
            _sdl3_mixer_c.Track.set_audiostream(self, audiostream)
        elif audiostream is None:
            _sdl3_mixer_c.Track.set_audiostream(self, None)
        else:
            raise TypeError(
                "audiostream argument must be an AudioStream or None, "
                f"received {type(audiostream)}"
            )
