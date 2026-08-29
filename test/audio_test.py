import unittest

import pygame

try:
    from pygame import _audio
except ImportError:
    _audio = None


@unittest.skipIf(_audio is None, "SDL3 audio API is unavailable")
class AudioFormatConversionTest(unittest.TestCase):
    def test_audio_formats_round_trip_through_stream(self):
        formats = (
            _audio.U8,
            _audio.S8,
            _audio.S16LE,
            _audio.S16BE,
            _audio.S32LE,
            _audio.S32BE,
            _audio.F32LE,
            _audio.F32BE,
        )

        for audio_format in formats:
            with self.subTest(audio_format=audio_format.name):
                spec = _audio.AudioSpec(audio_format, 2, 44100)
                stream = _audio.AudioStream(spec, spec)

                self.assertEqual(stream.src_spec.format, audio_format)
                self.assertEqual(stream.src_spec.channels, 2)
                self.assertEqual(stream.src_spec.frequency, 44100)
                self.assertEqual(stream.dst_spec.format, audio_format)
                self.assertEqual(stream.dst_spec.channels, 2)
                self.assertEqual(stream.dst_spec.frequency, 44100)

    def test_unknown_format_is_rejected_by_stream(self):
        spec = _audio.AudioSpec(_audio.UNKNOWN, 2, 44100)

        with self.assertRaises(pygame.error):
            _audio.AudioStream(spec, spec)


if __name__ == "__main__":
    unittest.main()
