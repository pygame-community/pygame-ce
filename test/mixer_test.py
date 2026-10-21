import copy
import os
import pathlib
import platform
import sys
import time
import unittest
from tempfile import TemporaryDirectory

import pygame
from pygame import mixer
from pygame.tests.test_utils import example_path, prompt, question

IS_PYPY = "PyPy" == platform.python_implementation()

################################### CONSTANTS ##################################

FREQUENCIES = [11025, 22050, 44100, 48000]
SIZES = [-16, -8, 8, 16]  # fixme
# size 32 failed in test_get_init__returns_exact_values_used_for_init
CHANNELS = [1, 2]
BUFFERS = [3024]

CONFIGS = [
    {"frequency": f, "size": s, "channels": c}
    for f in FREQUENCIES
    for s in SIZES
    for c in CHANNELS
]
# Using all CONFIGS fails on a Mac; probably older SDL_mixer; we could do:
# if platform.system() == 'Darwin':
# But using all CONFIGS is very slow (> 10 sec for example)
# And probably, we don't need to be so exhaustive, hence:

CONFIG = {"frequency": 44100, "size": 32, "channels": 2, "allowedchanges": 0}


class InvalidBool:
    """To help test invalid bool values."""

    __bool__ = None


def get_fake_sound_duration(duration_ms: int) -> mixer.Sound:
    """Generates a Sound object for the duration.
    Requires mixer to be initialized.
    """

    frequency, format, channels = mixer.get_init()

    format_bytes = abs(format) / 8
    if not format_bytes.is_integer():
        raise RuntimeError("This is a weird format, panic")
    format_bytes = int(format_bytes)

    # frequency = samples per second
    # format_bytes is number of bytes for each value, channels is number of values inside a sample

    audio_buf = bytes(format_bytes * channels * round(frequency / 1000 * duration_ms))
    return mixer.Sound(buffer=audio_buf)


############################## MODULE LEVEL TESTS #############################


class MixerModuleTest(unittest.TestCase):
    def tearDown(self):
        mixer.quit()
        mixer.pre_init(0, 0, 0, 0)

    def test_get_driver(self):
        mixer.init()
        drivers = [
            pygame.NULL_VIDEODRIVER,
            "pipewire",
            "pulseaudio",
            "alsa",
            "jack",
            "sndio",
            "netbsd",
            "dsp",
            "qsa",
            "audio",
            "arts",
            "esd",
            "nacl",
            "nas",
            "wasapi",
            "directsound",
            "winmm",
            "paud",
            "haiku",
            "coreaudio",
            "disk",
            "fusionsound",
            "AAudio",
            "openslES",
            "android",
            "ps2",
            "psp",
            "vita",
            "n3ds",
            "emscripten",
            "DART",
        ]
        driver = mixer.get_driver()
        self.assertIn(driver, drivers)

        mixer.quit()
        with self.assertRaises(pygame.error):
            mixer.get_driver()

    def test_init__keyword_args(self):
        # note: this test used to loop over all CONFIGS, but it's very slow..
        mixer.init(**CONFIG)
        mixer_conf = mixer.get_init()

        self.assertEqual(mixer_conf[0], CONFIG["frequency"])
        # Not all "sizes" are supported on all systems,  hence "abs".
        self.assertEqual(abs(mixer_conf[1]), abs(CONFIG["size"]))
        self.assertGreaterEqual(mixer_conf[2], CONFIG["channels"])

    def test_pre_init__keyword_args(self):
        # note: this test used to loop over all CONFIGS, but it's very slow..
        mixer.pre_init(**CONFIG)
        mixer.init()

        mixer_conf = mixer.get_init()

        self.assertEqual(mixer_conf[0], CONFIG["frequency"])
        # Not all "sizes" are supported on all systems,  hence "abs".
        self.assertEqual(abs(mixer_conf[1]), abs(CONFIG["size"]))
        self.assertGreaterEqual(mixer_conf[2], CONFIG["channels"])

    def test_pre_init__zero_values(self):
        # Ensure that argument values of 0 are replaced with
        # default values. No way to check buffer size though.
        mixer.pre_init(22050, -8, 1)  # Non default values
        mixer.pre_init(0, 0, 0)  # Should reset to default values
        mixer.init(allowedchanges=0)
        self.assertEqual(mixer.get_init()[0], 44100)
        self.assertEqual(mixer.get_init()[1], -16)
        self.assertGreaterEqual(mixer.get_init()[2], 2)

    def test_init__zero_values(self):
        # Ensure that argument values of 0 are replaced with
        # preset values. No way to check buffer size though.
        mixer.pre_init(44100, 8, 1, allowedchanges=0)  # None default values
        mixer.init(0, 0, 0)
        self.assertEqual(mixer.get_init(), (44100, 8, 1))

    def test_get_init__returns_exact_values_used_for_init(self):
        # TODO: size 32 fails in this test (maybe SDL_mixer bug)

        for init_conf in CONFIGS:
            frequency, size, channels = init_conf.values()
            if (frequency, size) == (22050, 16):
                continue
            mixer.init(frequency, size, channels, allowedchanges=0)

            mixer_conf = mixer.get_init()

            self.assertEqual(tuple(init_conf.values()), mixer_conf)
            mixer.quit()

    def test_get_init__returns_None_if_mixer_not_initialized(self):
        self.assertIsNone(mixer.get_init())

    def test_get_busy__returns_False_if_mixer_not_initialized(self):
        # get_busy() is documented to return False (not raise) when the mixer
        # has not been initialized.
        self.assertFalse(mixer.get_busy())

    def test_get_num_channels__defaults_eight_after_init(self):
        mixer.init()
        self.assertEqual(mixer.get_num_channels(), 8)

    def test_set_num_channels(self):
        mixer.init()

        default_num_channels = mixer.get_num_channels()
        for i in range(1, default_num_channels + 1):
            mixer.set_num_channels(i)
            self.assertEqual(mixer.get_num_channels(), i)

        # Growing past the default reallocates the internal channel array.
        mixer.set_num_channels(32)
        self.assertEqual(mixer.get_num_channels(), 32)

        # Shrinking stops any sound playing on a channel that goes away.
        sound = get_fake_sound_duration(500)
        mixer.Channel(20).play(sound)
        self.assertEqual(sound.get_num_channels(), 1)
        mixer.set_num_channels(8)
        self.assertEqual(mixer.get_num_channels(), 8)
        self.assertEqual(sound.get_num_channels(), 0)

        # Zero is allowed.
        mixer.set_num_channels(0)
        self.assertEqual(mixer.get_num_channels(), 0)

    def test_init__invalid_args(self):
        """Ensure init rejects an unsupported size and channel count."""
        # An unsupported sample size is rejected.
        with self.assertRaises(ValueError):
            mixer.init(44100, 24)
        # With allowedchanges=0 the channel count must be 1, 2, 4, or 6.
        with self.assertRaises(ValueError):
            mixer.init(44100, -16, 3, allowedchanges=0)

    def test_set_soundfont(self):
        """Ensure soundfonts can be set, cleared, and retrieved"""
        mixer.init()

        # test that initially, get_soundfont returns only real files
        if (initial_sf := mixer.get_soundfont()) is not None:
            for i in initial_sf.split(";"):
                os.path.exists(i)

        mixer.set_soundfont()
        self.assertEqual(mixer.get_soundfont(), None)

        mixer.set_soundfont(None)
        self.assertEqual(mixer.get_soundfont(), None)

        mixer.set_soundfont("test1.sf2;test2.sf2")
        self.assertEqual(mixer.get_soundfont(), "test1.sf2;test2.sf2")

        mixer.set_soundfont("")
        self.assertEqual(mixer.get_soundfont(), None)

        self.assertRaises(TypeError, mixer.set_soundfont, 0)
        self.assertRaises(TypeError, mixer.set_soundfont, ["one", "two"])

    def test_quit(self):
        """get_num_channels() Should throw pygame.error if uninitialized
        after mixer.quit()"""
        mixer.init()
        mixer.quit()
        self.assertRaises(pygame.error, mixer.get_num_channels)

    # TODO: FIXME: pypy (on linux) fails here sometimes.
    @unittest.skipIf(
        sys.maxsize <= 2**32,
        "randomly fails on comparing bytes",
    )
    @unittest.skipIf(IS_PYPY, "random errors here with pypy")
    def test_sound_args(self):
        def get_bytes(snd):
            return snd.get_raw()

        mixer.init()

        sample = b"\x00\xff" * 24
        wave_path = example_path(os.path.join("data", "house_lo.wav"))
        uwave_path = str(wave_path)
        bwave_path = uwave_path.encode(sys.getfilesystemencoding())
        snd = mixer.Sound(file=wave_path)
        self.assertTrue(snd.get_length() > 0.5)
        snd_bytes = get_bytes(snd)
        self.assertTrue(len(snd_bytes) > 1000)

        self.assertEqual(get_bytes(mixer.Sound(wave_path)), snd_bytes)

        self.assertEqual(get_bytes(mixer.Sound(file=uwave_path)), snd_bytes)
        self.assertEqual(get_bytes(mixer.Sound(uwave_path)), snd_bytes)
        arg_emsg = "Sound takes either 1 positional or 1 keyword argument"

        with self.assertRaises(TypeError) as cm:
            mixer.Sound()
        self.assertEqual(str(cm.exception), arg_emsg)
        with self.assertRaises(TypeError) as cm:
            mixer.Sound(wave_path, buffer=sample)
        self.assertEqual(str(cm.exception), arg_emsg)
        with self.assertRaises(TypeError) as cm:
            mixer.Sound(sample, file=wave_path)
        self.assertEqual(str(cm.exception), arg_emsg)
        with self.assertRaises(TypeError) as cm:
            mixer.Sound(buffer=sample, file=wave_path)
        self.assertEqual(str(cm.exception), arg_emsg)

        with self.assertRaises(TypeError) as cm:
            mixer.Sound(foobar=sample)
        self.assertEqual(str(cm.exception), "Unrecognized keyword argument 'foobar'")

        snd = mixer.Sound(wave_path, **{})
        self.assertEqual(get_bytes(snd), snd_bytes)
        snd = mixer.Sound(*[], **{"file": wave_path})

        with self.assertRaises(TypeError) as cm:
            mixer.Sound([])
        self.assertEqual(str(cm.exception), "Unrecognized argument (type list)")

        with self.assertRaises(TypeError) as cm:
            snd = mixer.Sound(buffer=[])
        emsg = "Expected object with buffer interface: got a list"
        self.assertEqual(str(cm.exception), emsg)

        ufake_path = "12345678"
        self.assertRaises(IOError, mixer.Sound, ufake_path)
        self.assertRaises(IOError, mixer.Sound, "12345678")

        with self.assertRaises(TypeError) as cm:
            mixer.Sound(buffer="something")
        emsg = "Unicode object not allowed as buffer object"
        self.assertEqual(str(cm.exception), emsg)
        self.assertEqual(get_bytes(mixer.Sound(buffer=sample)), sample)
        if type(sample) != str:
            somebytes = get_bytes(mixer.Sound(sample))
            # on python 2 we do not allow using string except as file name.
            self.assertEqual(somebytes, sample)
        self.assertEqual(get_bytes(mixer.Sound(file=bwave_path)), snd_bytes)
        self.assertEqual(get_bytes(mixer.Sound(bwave_path)), snd_bytes)

        snd = mixer.Sound(wave_path)
        with self.assertRaises(TypeError) as cm:
            mixer.Sound(wave_path, array=snd)
        self.assertEqual(str(cm.exception), arg_emsg)
        with self.assertRaises(TypeError) as cm:
            mixer.Sound(buffer=sample, array=snd)
        self.assertEqual(str(cm.exception), arg_emsg)
        snd2 = mixer.Sound(array=snd)
        self.assertEqual(snd.get_raw(), snd2.get_raw())

    def test_sound_unicode(self):
        """test non-ASCII unicode path"""
        mixer.init()
        import shutil

        ep = example_path("data")
        with TemporaryDirectory() as tmpdir:
            temp_file = os.path.join(tmpdir, "你好.wav")
            org_file = os.path.join(ep, "house_lo.wav")
            shutil.copy(org_file, temp_file)
            sound = mixer.Sound(temp_file)
            del sound

    @unittest.skipIf(
        os.environ.get("SDL_AUDIODRIVER") == "disk",
        "this test fails without real sound card",
    )
    def test_array_keyword(self):
        try:
            from numpy import (
                arange,
                array,
                int8,
                int16,
                int32,
                uint8,
                uint16,
                uint32,
                zeros,
            )
        except ImportError:
            self.skipTest("requires numpy")

        freq = 22050
        format_list = [-8, 8, -16, 16]
        channels_list = [1, 2]

        a_lists = {f: [] for f in format_list}
        a32u_mono = arange(0, 256, 1, uint32)
        a16u_mono = a32u_mono.astype(uint16)
        a8u_mono = a32u_mono.astype(uint8)
        au_list_mono = [(1, a) for a in [a8u_mono, a16u_mono, a32u_mono]]
        for format in format_list:
            if format > 0:
                a_lists[format].extend(au_list_mono)
        a32s_mono = arange(-128, 128, 1, int32)
        a16s_mono = a32s_mono.astype(int16)
        a8s_mono = a32s_mono.astype(int8)
        as_list_mono = [(1, a) for a in [a8s_mono, a16s_mono, a32s_mono]]
        for format in format_list:
            if format < 0:
                a_lists[format].extend(as_list_mono)
        a32u_stereo = zeros([a32u_mono.shape[0], 2], uint32)
        a32u_stereo[:, 0] = a32u_mono
        a32u_stereo[:, 1] = 255 - a32u_mono
        a16u_stereo = a32u_stereo.astype(uint16)
        a8u_stereo = a32u_stereo.astype(uint8)
        au_list_stereo = [(2, a) for a in [a8u_stereo, a16u_stereo, a32u_stereo]]
        for format in format_list:
            if format > 0:
                a_lists[format].extend(au_list_stereo)
        a32s_stereo = zeros([a32s_mono.shape[0], 2], int32)
        a32s_stereo[:, 0] = a32s_mono
        a32s_stereo[:, 1] = -1 - a32s_mono
        a16s_stereo = a32s_stereo.astype(int16)
        a8s_stereo = a32s_stereo.astype(int8)
        as_list_stereo = [(2, a) for a in [a8s_stereo, a16s_stereo, a32s_stereo]]
        for format in format_list:
            if format < 0:
                a_lists[format].extend(as_list_stereo)

        for format in format_list:
            for channels in channels_list:
                try:
                    mixer.init(freq, format, channels)
                except pygame.error:
                    # Some formats (e.g. 16) may not be supported.
                    continue
                try:
                    __, f, c = mixer.get_init()
                    if f != format or c != channels:
                        # Some formats (e.g. -8) may not be supported.
                        continue
                    for c, a in a_lists[format]:
                        self._test_array_argument(format, a, c == channels)
                finally:
                    mixer.quit()

    def _test_array_argument(self, format, a, test_pass):
        from numpy import all as all_, array

        try:
            snd = mixer.Sound(array=a)
        except ValueError:
            if not test_pass:
                return
            self.fail("Raised ValueError: Format %i, dtype %s" % (format, a.dtype))
        if not test_pass:
            self.fail(
                "Did not raise ValueError: Format %i, dtype %s" % (format, a.dtype)
            )
        a2 = array(snd)
        a3 = a.astype(a2.dtype)
        lshift = abs(format) - 8 * a.itemsize
        if lshift >= 0:
            # This is asymmetric with respect to downcasting.
            a3 <<= lshift
        self.assertTrue(all_(a2 == a3), "Format %i, dtype %s" % (format, a.dtype))

    def _test_array_interface_fail(self, a):
        self.assertRaises(ValueError, mixer.Sound, array=a)

    def test_array_interface(self):
        mixer.init(22050, -16, 1, allowedchanges=0)
        snd = mixer.Sound(buffer=b"\x00\x7f" * 20)
        d = snd.__array_interface__
        self.assertTrue(isinstance(d, dict))
        if pygame.get_sdl_byteorder() == pygame.LIL_ENDIAN:
            typestr = "<i2"
        else:
            typestr = ">i2"
        self.assertEqual(d["typestr"], typestr)
        self.assertEqual(d["shape"], (20,))
        self.assertEqual(d["strides"], (2,))
        self.assertEqual(d["data"], (snd._samples_address, False))

    @unittest.skipIf(IS_PYPY, "pypy no likey")
    def test_newbuf__one_channel(self):
        mixer.init(22050, -16, 1)
        self._NEWBUF_export_check()

    @unittest.skipIf(IS_PYPY, "pypy no likey")
    def test_newbuf__twho_channel(self):
        mixer.init(22050, -16, 2)
        self._NEWBUF_export_check()

    def _NEWBUF_export_check(self):
        freq, fmt, channels = mixer.get_init()
        ndim = 1 if (channels == 1) else 2
        itemsize = abs(fmt) // 8
        formats = {
            8: "B",
            -8: "b",
            16: "=H",
            -16: "=h",
            32: "=I",
            -32: "=i",  # 32 and 64 for future consideration
            64: "=Q",
            -64: "=q",
        }
        format = formats[fmt]
        from pygame.tests.test_utils import buftools

        Exporter = buftools.Exporter
        Importer = buftools.Importer
        is_lil_endian = pygame.get_sdl_byteorder() == pygame.LIL_ENDIAN
        fsys, frev = ("<", ">") if is_lil_endian else (">", "<")
        shape = (10, channels)[:ndim]
        strides = (channels * itemsize, itemsize)[2 - ndim :]
        exp = Exporter(shape, format=frev + "i")
        snd = mixer.Sound(array=exp)
        buflen = len(exp) * itemsize * channels
        imp = Importer(snd, buftools.PyBUF_SIMPLE)
        self.assertEqual(imp.ndim, 0)
        self.assertTrue(imp.format is None)
        self.assertEqual(imp.len, buflen)
        self.assertEqual(imp.itemsize, itemsize)
        self.assertTrue(imp.shape is None)
        self.assertTrue(imp.strides is None)
        self.assertTrue(imp.suboffsets is None)
        self.assertFalse(imp.readonly)
        self.assertEqual(imp.buf, snd._samples_address)
        imp = Importer(snd, buftools.PyBUF_WRITABLE)
        self.assertEqual(imp.ndim, 0)
        self.assertTrue(imp.format is None)
        self.assertEqual(imp.len, buflen)
        self.assertEqual(imp.itemsize, itemsize)
        self.assertTrue(imp.shape is None)
        self.assertTrue(imp.strides is None)
        self.assertTrue(imp.suboffsets is None)
        self.assertFalse(imp.readonly)
        self.assertEqual(imp.buf, snd._samples_address)
        imp = Importer(snd, buftools.PyBUF_FORMAT)
        self.assertEqual(imp.ndim, 0)
        self.assertEqual(imp.format, format)
        self.assertEqual(imp.len, buflen)
        self.assertEqual(imp.itemsize, itemsize)
        self.assertTrue(imp.shape is None)
        self.assertTrue(imp.strides is None)
        self.assertTrue(imp.suboffsets is None)
        self.assertFalse(imp.readonly)
        self.assertEqual(imp.buf, snd._samples_address)
        imp = Importer(snd, buftools.PyBUF_ND)
        self.assertEqual(imp.ndim, ndim)
        self.assertTrue(imp.format is None)
        self.assertEqual(imp.len, buflen)
        self.assertEqual(imp.itemsize, itemsize)
        self.assertEqual(imp.shape, shape)
        self.assertTrue(imp.strides is None)
        self.assertTrue(imp.suboffsets is None)
        self.assertFalse(imp.readonly)
        self.assertEqual(imp.buf, snd._samples_address)
        imp = Importer(snd, buftools.PyBUF_STRIDES)
        self.assertEqual(imp.ndim, ndim)
        self.assertTrue(imp.format is None)
        self.assertEqual(imp.len, buflen)
        self.assertEqual(imp.itemsize, itemsize)
        self.assertEqual(imp.shape, shape)
        self.assertEqual(imp.strides, strides)
        self.assertTrue(imp.suboffsets is None)
        self.assertFalse(imp.readonly)
        self.assertEqual(imp.buf, snd._samples_address)
        imp = Importer(snd, buftools.PyBUF_FULL_RO)
        self.assertEqual(imp.ndim, ndim)
        self.assertEqual(imp.format, format)
        self.assertEqual(imp.len, buflen)
        self.assertEqual(imp.itemsize, 2)
        self.assertEqual(imp.shape, shape)
        self.assertEqual(imp.strides, strides)
        self.assertTrue(imp.suboffsets is None)
        self.assertFalse(imp.readonly)
        self.assertEqual(imp.buf, snd._samples_address)
        imp = Importer(snd, buftools.PyBUF_FULL_RO)
        self.assertEqual(imp.ndim, ndim)
        self.assertEqual(imp.format, format)
        self.assertEqual(imp.len, buflen)
        self.assertEqual(imp.itemsize, itemsize)
        self.assertEqual(imp.shape, exp.shape)
        self.assertEqual(imp.strides, strides)
        self.assertTrue(imp.suboffsets is None)
        self.assertFalse(imp.readonly)
        self.assertEqual(imp.buf, snd._samples_address)
        imp = Importer(snd, buftools.PyBUF_C_CONTIGUOUS)
        self.assertEqual(imp.ndim, ndim)
        self.assertTrue(imp.format is None)
        self.assertEqual(imp.strides, strides)
        imp = Importer(snd, buftools.PyBUF_ANY_CONTIGUOUS)
        self.assertEqual(imp.ndim, ndim)
        self.assertTrue(imp.format is None)
        self.assertEqual(imp.strides, strides)
        if ndim == 1:
            imp = Importer(snd, buftools.PyBUF_F_CONTIGUOUS)
            self.assertEqual(imp.ndim, 1)
            self.assertTrue(imp.format is None)
            self.assertEqual(imp.strides, strides)
        else:
            self.assertRaises(BufferError, Importer, snd, buftools.PyBUF_F_CONTIGUOUS)

    def test_find_channel(self):
        # __doc__ (as of 2008-08-02) for pygame.mixer.find_channel:

        # pygame.mixer.find_channel(force=False): return Channel
        # find an unused channel
        mixer.init()

        filename = example_path(os.path.join("data", "house_lo.wav"))
        sound = mixer.Sound(file=filename)

        if (num_channels := mixer.get_num_channels()) > 0:
            found_channel = mixer.find_channel()
            self.assertIsNotNone(found_channel)

            # try playing on all channels
            channels = []
            for channel_id in range(0, num_channels):
                channel = mixer.Channel(channel_id)
                channel.play(sound)
                channels.append(channel)

            # should fail without being forceful
            found_channel = mixer.find_channel()
            self.assertIsNone(found_channel)

            # try forcing without keyword
            found_channel = mixer.find_channel(True)
            self.assertIsNotNone(found_channel)

            # try forcing with keyword
            found_channel = mixer.find_channel(force=True)
            self.assertIsNotNone(found_channel)

            for channel in channels:
                channel.stop()
            found_channel = mixer.find_channel()
            self.assertIsNotNone(found_channel)

    def test_set_reserved(self):
        # __doc__ (as of 2008-08-02) for pygame.mixer.set_reserved:

        # pygame.mixer.set_reserved(count): return count
        mixer.init()
        default_num_channels = mixer.get_num_channels()

        # try reserving all the channels
        result = mixer.set_reserved(default_num_channels)
        self.assertEqual(result, default_num_channels)

        # try reserving all the channels + 1
        result = mixer.set_reserved(default_num_channels + 1)
        # should still be default
        self.assertEqual(result, default_num_channels)

        # try unreserving all
        result = mixer.set_reserved(0)
        # should still be default
        self.assertEqual(result, 0)

        # try reserving half
        result = mixer.set_reserved(int(default_num_channels / 2))
        # should still be default
        self.assertEqual(result, int(default_num_channels / 2))

    def test_get_sdl_mixer_version(self):
        """Ensures get_sdl_mixer_version works correctly with no args."""
        expected_length = 3
        expected_type = tuple
        expected_item_type = int

        version = pygame.mixer.get_sdl_mixer_version()

        self.assertIsInstance(version, expected_type)
        self.assertEqual(len(version), expected_length)

        for item in version:
            self.assertIsInstance(item, expected_item_type)

    def test_get_sdl_mixer_version__args(self):
        """Ensures get_sdl_mixer_version works correctly using args."""
        expected_length = 3
        expected_type = tuple
        expected_item_type = int

        for value in (True, False):
            version = pygame.mixer.get_sdl_mixer_version(value)

            self.assertIsInstance(version, expected_type)
            self.assertEqual(len(version), expected_length)

            for item in version:
                self.assertIsInstance(item, expected_item_type)

    def test_get_sdl_mixer_version__kwargs(self):
        """Ensures get_sdl_mixer_version works correctly using kwargs."""
        expected_length = 3
        expected_type = tuple
        expected_item_type = int

        for value in (True, False):
            version = pygame.mixer.get_sdl_mixer_version(linked=value)

            self.assertIsInstance(version, expected_type)
            self.assertEqual(len(version), expected_length)

            for item in version:
                self.assertIsInstance(item, expected_item_type)

    def test_get_sdl_mixer_version__invalid_args_kwargs(self):
        """Ensures get_sdl_mixer_version handles invalid args and kwargs."""
        invalid_bool = InvalidBool()

        with self.assertRaises(TypeError):
            version = pygame.mixer.get_sdl_mixer_version(invalid_bool)

        with self.assertRaises(TypeError):
            version = pygame.mixer.get_sdl_mixer_version(linked=invalid_bool)

    def test_get_sdl_mixer_version__linked_equals_compiled(self):
        """Ensures get_sdl_mixer_version's linked/compiled versions are equal."""
        linked_version = pygame.mixer.get_sdl_mixer_version(linked=True)
        compiled_version = pygame.mixer.get_sdl_mixer_version(linked=False)

        self.assertTupleEqual(linked_version, compiled_version)


########################### MODULE PLAYBACK TESTS ############################


class MixerPlaybackTest(unittest.TestCase):
    """Tests for the module-level controls that act on all channels at once:
    stop(), pause(), unpause(), fadeout() and get_busy().
    """

    @classmethod
    def setUpClass(cls):
        # Initializing the mixer is slow, so minimize the times it is called.
        mixer.init()

    @classmethod
    def tearDownClass(cls):
        mixer.quit()

    def setUp(self):
        # Make sure the mixer is initialized before each test (in case a
        # previous test quit it).
        if mixer.get_init() is None:
            mixer.init()

    def tearDown(self):
        # Every test here drives global playback and pausing. Reset that state
        # so nothing leaks into the next test, even if an assert failed early.
        mixer.stop()
        mixer.unpause()

    def test_get_busy(self):
        """get_busy() reflects whether any channel is mixing."""
        self.assertFalse(mixer.get_busy())

        sound = get_fake_sound_duration(200)
        sound.play()
        self.assertTrue(mixer.get_busy())

        mixer.stop()
        self.assertFalse(mixer.get_busy())

    def test_stop(self):
        """stop() halts playback on every channel."""
        sound = get_fake_sound_duration(200)
        sound.play()
        sound.play()
        self.assertEqual(sound.get_num_channels(), 2)

        mixer.stop()
        self.assertEqual(sound.get_num_channels(), 0)
        self.assertFalse(mixer.get_busy())

    def test_pause_unpause(self):
        """pause() freezes all channels; unpause() resumes them."""
        mixer.unpause()  # legal to call with nothing playing
        mixer.pause()

        sound = get_fake_sound_duration(10)

        # Playback starts even if pause() was the last call.
        sound.play()
        self.assertTrue(mixer.get_busy())

        mixer.pause()
        pygame.time.wait(30)  # 3x the sound length
        self.assertTrue(
            mixer.get_busy(), "a paused channel stays busy past the sound length"
        )

        mixer.unpause()
        start = pygame.time.get_ticks()
        while mixer.get_busy() and pygame.time.get_ticks() - start < 200:
            pygame.time.wait(1)
        self.assertFalse(mixer.get_busy(), "unpaused playback should finish")

    def test_fadeout(self):
        """fadeout() fades and stops all channels within the fade time."""
        sound = get_fake_sound_duration(500)
        sound.play()
        sound.play()

        mixer.fadeout(50)
        pygame.time.wait(1)
        self.assertTrue(mixer.get_busy())  # still fading right after
        pygame.time.wait(75)
        self.assertFalse(mixer.get_busy())  # faded out and stopped

    def test_stop__discards_queue(self):
        """stop() discards a queued Sound rather than advancing to it."""
        queued = get_fake_sound_duration(300)
        ch = mixer.Channel(0)
        ch.play(get_fake_sound_duration(10), loops=-1)  # loop so it can't end
        ch.queue(queued)

        mixer.stop()
        self.assertIsNone(
            ch.get_sound(), "mixer.stop() should not advance to the queued sound"
        )

    def test_fadeout__keeps_queue(self):
        """fadeout() lets the queued Sound play once the fade completes."""
        queued = get_fake_sound_duration(300)
        ch = mixer.Channel(0)
        ch.play(get_fake_sound_duration(10), loops=-1)  # loop so it can't end
        ch.queue(queued)

        mixer.fadeout(10)
        advanced = False
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < 200:
            pygame.time.wait(1)
            if ch.get_sound() == queued:
                advanced = True
                break
        self.assertTrue(advanced, "mixer.fadeout() should let the queued sound play")


############################## CHANNEL CLASS TESTS #############################


class ChannelTypeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initializing the mixer is slow, so minimize the times it is called.
        mixer.init()

    @classmethod
    def tearDownClass(cls):
        mixer.quit()

    def setUp(cls):
        # This makes sure the mixer is always initialized before each test (in
        # case a test calls pygame.mixer.quit()).
        if mixer.get_init() is None:
            mixer.init()

    def test_channel_alias(self):
        """Check if pygame.Channel is present and the correct type."""
        self.assertIs(pygame.Channel, pygame.mixer.Channel)

    def test_channel(self):
        """Ensure Channel() creation works."""
        channel = mixer.Channel(0)

        self.assertIsInstance(channel, mixer.ChannelType)
        self.assertEqual(channel.__class__.__name__, "Channel")

    def test_channel__without_arg(self):
        """Ensure exception for Channel() creation with no argument."""
        with self.assertRaises(TypeError):
            mixer.Channel()

    def test_channel__invalid_id(self):
        """Ensure exception for Channel() creation with an invalid id."""
        with self.assertRaises(IndexError):
            mixer.Channel(-1)
        with self.assertRaises(IndexError):
            mixer.Channel(mixer.get_num_channels())  # one past the last valid id

    def test_channel__before_init(self):
        """Ensure exception for Channel() creation with non-init mixer."""
        mixer.quit()

        with self.assertRaisesRegex(pygame.error, "mixer not initialized"):
            mixer.Channel(0)

    def test_fadeout(self):
        """Test fadeout exists, and stops playback in reasonable time."""

        filename = example_path(os.path.join("data", "house_lo.wav"))
        sound = mixer.Sound(filename)

        ch = mixer.Channel(0)
        ch.play(sound)
        ch.fadeout(50)
        pygame.time.wait(1)
        self.assertTrue(ch.get_busy())  # After 1 ms it is still running
        pygame.time.wait(75)
        self.assertFalse(ch.get_busy())  # After 75 ms it should be stopped
        ch.stop()  # just to be sure

    def test_get_busy(self):
        """Ensure an idle channel's busy state is correct."""
        expected_busy = False
        channel = mixer.Channel(0)

        busy = channel.get_busy()

        self.assertEqual(busy, expected_busy)

    def test_get_busy__active(self):
        """Ensure an active channel's busy state is correct."""

        filename = example_path(os.path.join("data", "house_lo.wav"))
        sound = mixer.Sound(filename)

        ch = mixer.Channel(0)
        ch.play(sound)
        try:
            self.assertTrue(ch.get_busy())
        finally:
            ch.stop()

    def test_queue_and_get(self):
        """Test channel queue system."""

        sound1 = get_fake_sound_duration(10)
        sound2 = get_fake_sound_duration(300)

        ch0 = mixer.Channel(0)
        ch1 = mixer.Channel(1)

        try:
            ch0.play(sound2)
            ch0.queue(sound1)
            ch0.play(sound2)
            self.assertIsNone(ch0.get_queue(), "play should nullify queue")
            ch0.stop()

            ch1.play(sound1, loops=-1)  # loop so can't end on its own
            ch1.queue(sound2)
            ch1.stop()  # stop() discards the queue
            self.assertIsNone(
                ch1.get_sound(), "stop should not advance to the queued sound"
            )
            ch1.stop()  # Just in case

            # fadeout() is not a hard stop: the queued sound still plays once
            # the fade completes (this differs from stop()).
            ch1.play(sound1, loops=-1)  # loop so can't end on its own
            ch1.queue(sound2)
            ch1.fadeout(10)
            advanced_after_fadeout = False
            start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start < 200:
                pygame.time.wait(1)
                if ch1.get_sound() == sound2:
                    advanced_after_fadeout = True
                    break
            self.assertTrue(
                advanced_after_fadeout, "fadeout should let the queued sound play"
            )
            ch1.stop()  # Just in case

            # If we play a 10 ms sound, and queue a 300 ms sound, we should
            # see that it has advanced to the queued sound within 100 ms.
            ch1.play(sound1)
            ch1.queue(sound2)
            advanced_to_sound2 = False
            start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start < 200:
                pygame.time.wait(1)
                if ch1.get_sound() is sound2:
                    advanced_to_sound2 = True
                    break
            self.assertTrue(advanced_to_sound2)

        finally:
            ch0.stop()
            ch1.stop()

    def test_play__rejects_non_sound(self):
        """Channel.play requires a Sound argument."""
        ch = mixer.Channel(0)
        with self.assertRaises(TypeError):
            ch.play("not a sound")

    def test_queue__rejects_non_sound(self):
        """Channel.queue requires a Sound argument."""
        ch = mixer.Channel(0)
        with self.assertRaises(TypeError):
            ch.queue(42)

    def test_queue__nothing_playing(self):
        """Queueing on an idle channel starts playback immediately."""
        sound = get_fake_sound_duration(200)

        ch = mixer.Channel(0)
        self.assertIsNone(ch.get_sound())
        try:
            ch.queue(sound)
            self.assertIs(ch.get_sound(), sound)
            self.assertIsNone(ch.get_queue())
            self.assertTrue(ch.get_busy())
        finally:
            ch.stop()

    def test_get_sound(self):
        """Test get sound initial and when playing"""

        filename = example_path(os.path.join("data", "house_lo.wav"))
        sound = mixer.Sound(filename)

        ch = mixer.Channel(0)
        self.assertIsNone(ch.get_sound())
        ch.play(sound)
        self.assertEqual(ch.get_sound(), sound)
        ch.stop()
        self.assertIsNone(ch.get_sound())

    def test_get_volume(self):
        """Ensure a channel's volume can be retrieved."""
        expected_volume = 1.0  # default
        channel = mixer.Channel(0)

        volume = channel.get_volume()

        self.assertAlmostEqual(volume, expected_volume)

    def test_volume_active(self):
        """Test getting and setting a volume with some playback."""

        filename = example_path(os.path.join("data", "house_lo.wav"))
        sound = mixer.Sound(filename)

        ch = mixer.Channel(0)

        with self.assertRaises(TypeError):
            ch.set_volume("0", "1")

        ch.set_volume(23, -1)
        self.assertEqual(ch.get_volume(), 1.0)
        ch.set_volume(0.8)
        self.assertAlmostEqual(ch.get_volume(), 0.8, places=2)

        try:
            ch.play(sound)
            self.assertAlmostEqual(ch.get_volume(), 0.8, places=2)
            ch.set_volume(0.2)
            self.assertAlmostEqual(ch.get_volume(), 0.2, places=2)
        finally:
            ch.stop()

    def test_pause_unpause(self):
        """Test pausing and unpausing a channel."""

        sound = get_fake_sound_duration(10)

        ch = mixer.Channel(0)
        ch.unpause()  # Legal to pause and unpause without anything playing
        ch.pause()

        # Playing a sound will actually play even if pause was the last thing called
        ch.play(sound)
        try:
            self.assertTrue(ch.get_busy())
            ch.pause()
            pygame.time.wait(30)
            self.assertTrue(
                ch.get_busy(),
                "paused still = busy, and we've waited 3x duration, so it must be really paused",
            )

            ch.unpause()
            start = pygame.time.get_ticks()
            while ch.get_busy() and pygame.time.get_ticks() - start < 200:
                pygame.time.wait(1)
            self.assertFalse(
                ch.get_busy(), "unpaused channel should play out and finish"
            )
        finally:
            ch.stop()

    def test_play(self):
        """Test active play and params."""

        sound = get_fake_sound_duration(10)

        ch = mixer.Channel(0)

        try:
            ch.play(sound)
            self.assertTrue(ch.get_busy())
            start = pygame.time.get_ticks()
            ch_stopped = False
            while pygame.time.get_ticks() - start < 50:
                if not ch.get_busy():
                    ch_stopped = True
                    break
                pygame.time.wait(1)
            self.assertTrue(ch_stopped)

            # Looping extends duration
            ch.stop()
            ch.play(sound, 100)
            pygame.time.wait(30)  # 3x duration
            self.assertTrue(ch.get_busy(), "looping channel should still be playing")

            # Maxtime, poll for it to stop with a ceiling for slow test runners
            ch.stop()
            ch.play(sound, -1, 50)
            start = pygame.time.get_ticks()
            while ch.get_busy() and pygame.time.get_ticks() - start < 200:
                pygame.time.wait(1)
            self.assertFalse(ch.get_busy(), "maxtime should have halted the channel")
        finally:
            ch.stop()

    def test_set_endevent(self):
        """Test setting and sending endevents."""

        filename = example_path(os.path.join("data", "house_lo.wav"))
        sound = mixer.Sound(filename)

        ch = mixer.Channel(0)
        event_type = pygame.event.custom_type()

        try:
            # Test it rejects invalid types
            with self.assertRaises(TypeError):
                ch.set_endevent("hello world")

            ch.set_endevent(event_type)

            # Test it doesn't fail when display is not around
            pygame.display.quit()
            ch.play(sound)
            ch.stop()
            pygame.time.delay(1)
            self.assertFalse(
                ch.get_busy(),
                "Channel should be no longer busy, and should not have crashed",
            )

            # When display (event system) is around, it should post the event
            pygame.display.init()
            ch.play(sound)
            ch.stop()
            pygame.time.delay(1)
            self.assertEqual(
                len([ev for ev in pygame.event.get() if ev.type == event_type]),
                1,
                "there should be exactly one event_type event in the queue",
            )

        finally:
            ch.stop()
            ch.set_endevent()  # Clear end event
            pygame.display.quit()

    def test_get_endevent(self):
        """Test endevent initial value, get/set"""

        ch = mixer.Channel(0)
        event_type = pygame.event.custom_type()

        self.assertEqual(ch.get_endevent(), pygame.NOEVENT)
        ch.set_endevent(event_type)
        self.assertEqual(ch.get_endevent(), event_type)
        ch.set_endevent()  # Clear end event

    def test_set_source_location(self):
        ch = mixer.Channel(0)
        ch.set_source_location(-3.14, 6.25)
        self.assertRaises(ValueError, lambda: ch.set_source_location(0, -1))
        self.assertRaises(ValueError, lambda: ch.set_source_location(0, 256.0))
        self.assertRaises(TypeError, lambda: ch.set_source_location("", 6.25))

    def test_id_getter(self):
        ch1 = mixer.Channel(1)
        ch2 = mixer.Channel(2)

        self.assertEqual(ch1.id, 1)
        self.assertEqual(ch2.id, 2)

    def test_subclass(self):
        class MyChannel(mixer.Channel):
            pass


class ChannelInteractiveTest(unittest.TestCase):
    __tags__ = ["interactive"]

    def tearDown(self):
        mixer.quit()
        mixer.pre_init(0, 0, 0, 0)

    def setUp(self):
        mixer.init()
        filename = example_path(os.path.join("data", "house_lo.mp3"))
        self.snd = mixer.Sound(filename)

    def test_set_source_location(self):
        prompt("Please wear earphones before the test for set_source_location() starts")
        ch = self.snd.play()
        angle = 0
        distance = 100
        while ch.get_busy():
            ch.set_source_location(angle, distance)
            angle += 1
            angle %= 360
            time.sleep(0.01)
        ans = question("You heard the sound was running around you. Is that correct?")
        self.assertTrue(ans)

        ch = self.snd.play()
        angle = 0
        distance = 0
        direction = 0
        while ch.get_busy():
            ch.set_source_location(angle, distance)
            if distance == 0 or distance == 255:
                direction = 1 - direction
            distance += 1 if direction else -1
            time.sleep(0.01)

        ans = question(
            "You heard the distance of the sound was changing. Is that correct?"
        )
        self.assertTrue(ans)


############################### SOUND CLASS TESTS ##############################


class SoundTypeTest(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        mixer.quit()

    def setUp(cls):
        # This makes sure the mixer is always initialized before each test (in
        # case a test calls pygame.mixer.quit()).
        if mixer.get_init() is None:
            mixer.init()

    # See MixerModuleTest's methods test_sound_args(), test_sound_unicode(),
    # and test_array_keyword() for additional testing of Sound() creation.
    def test_sound(self):
        """Ensure Sound() creation with a filename works."""
        filename = example_path(os.path.join("data", "house_lo.wav"))
        sound1 = mixer.Sound(filename)
        sound2 = mixer.Sound(file=filename)

        self.assertIsInstance(sound1, mixer.Sound)
        self.assertIsInstance(sound2, mixer.Sound)

    def test_sound__from_file_object(self):
        """Ensure Sound() creation with a file object works."""
        filename = example_path(os.path.join("data", "house_lo.wav"))

        # Using 'with' ensures the file is closed even if test fails.
        with open(filename, "rb") as file_obj:
            sound = mixer.Sound(file_obj)

            self.assertIsInstance(sound, mixer.Sound)

    def test_sound__from_sound_object(self):
        """Ensure Sound() creation with a Sound() object works."""
        filename = example_path(os.path.join("data", "house_lo.wav"))
        sound_obj = mixer.Sound(file=filename)

        sound = mixer.Sound(sound_obj)

        self.assertIsInstance(sound, mixer.Sound)

    def test_sound__from_pathlib(self):
        """Ensure Sound() creation with a pathlib.Path object works."""
        path = pathlib.Path(example_path(os.path.join("data", "house_lo.wav")))
        sound1 = mixer.Sound(path)
        sound2 = mixer.Sound(file=path)
        self.assertIsInstance(sound1, mixer.Sound)
        self.assertIsInstance(sound2, mixer.Sound)

        self.assertRaises(
            FileNotFoundError, mixer.Sound, pathlib.Path("/aWH8ryIyWt5BL7xf327e")
        )  # this path should not exist on any system really

    # Sound() creation from a buffer and from an array is covered by
    # MixerModuleTest.test_sound_args() and test_array_keyword().

    def test_sound_alias(self):
        """Check pygame.Sound is present and is the same type."""
        self.assertIs(pygame.Sound, pygame.mixer.Sound)

    def test_sound__without_arg(self):
        """Ensure exception raised for Sound() creation with no argument."""
        with self.assertRaises(TypeError):
            mixer.Sound()

    def test_sound__before_init(self):
        """Ensure exception raised for Sound() creation with non-init mixer."""
        mixer.quit()
        filename = example_path(os.path.join("data", "house_lo.wav"))

        with self.assertRaisesRegex(pygame.error, "mixer not initialized"):
            mixer.Sound(file=filename)

    @unittest.skipIf(IS_PYPY, "pypy skip")
    def test_samples_address(self):
        """Test the _samples_address getter."""
        try:
            from ctypes import c_void_p, py_object, pythonapi

            Bytes_FromString = pythonapi.PyBytes_FromString

            Bytes_FromString.restype = c_void_p
            Bytes_FromString.argtypes = [py_object]
            samples = b"abcdefgh"  # keep byte size a multiple of 4
            sample_bytes = Bytes_FromString(samples)

            snd = mixer.Sound(buffer=samples)

            self.assertNotEqual(snd._samples_address, sample_bytes)
        finally:
            pygame.mixer.quit()
            with self.assertRaisesRegex(pygame.error, "mixer not initialized"):
                snd._samples_address

    def test_fadeout(self):
        """Ensure Sound.fadeout stops playback within the fade time."""
        sound = get_fake_sound_duration(200)

        try:
            sound.play()
            sound.fadeout(50)
            pygame.time.wait(1)
            self.assertEqual(sound.get_num_channels(), 1)  # still running
            pygame.time.wait(75)
            self.assertEqual(sound.get_num_channels(), 0)  # faded out and stopped
        finally:
            sound.stop()

    def test_get_length(self):
        """Tests if get_length returns a correct length."""
        try:
            for size in SIZES:
                pygame.mixer.quit()
                pygame.mixer.init(size=size)
                filename = example_path(os.path.join("data", "punch.wav"))
                sound = mixer.Sound(file=filename)
                # The sound data is in the mixer output format. So dividing the
                # length of the raw sound data by the mixer settings gives
                # the expected length of the sound.
                sound_bytes = sound.get_raw()
                mix_freq, mix_bits, mix_channels = pygame.mixer.get_init()
                mix_bytes = abs(mix_bits) / 8
                expected_length = (
                    float(len(sound_bytes)) / mix_freq / mix_bytes / mix_channels
                )
                self.assertAlmostEqual(expected_length, sound.get_length())
        finally:
            pygame.mixer.quit()
            with self.assertRaisesRegex(pygame.error, "mixer not initialized"):
                sound.get_length()

    def test_get_num_channels(self):
        """
        Tests if Sound.get_num_channels returns the correct number
        of channels playing a specific sound.
        """
        try:
            filename = example_path(os.path.join("data", "house_lo.wav"))
            sound = mixer.Sound(file=filename)

            self.assertEqual(sound.get_num_channels(), 0)
            sound.play()
            self.assertEqual(sound.get_num_channels(), 1)
            sound.play()
            self.assertEqual(sound.get_num_channels(), 2)
            sound.stop()
            self.assertEqual(sound.get_num_channels(), 0)
        finally:
            pygame.mixer.quit()
            with self.assertRaisesRegex(pygame.error, "mixer not initialized"):
                sound.get_num_channels()

    def test_get_volume(self):
        """Ensure a sound's volume can be retrieved."""
        try:
            expected_volume = 1.0  # default
            filename = example_path(os.path.join("data", "house_lo.wav"))
            sound = mixer.Sound(file=filename)

            volume = sound.get_volume()

            self.assertAlmostEqual(volume, expected_volume)
        finally:
            pygame.mixer.quit()
            with self.assertRaisesRegex(pygame.error, "mixer not initialized"):
                sound.get_volume()

    def test_play(self):
        """Test Sound.play return value and loops/maxtime/fade_ms params."""
        sound = get_fake_sound_duration(10)

        try:
            # A plain play picks a channel, returns it, and starts playback
            channel = sound.play()
            self.assertIsInstance(channel, mixer.Channel)
            self.assertIs(channel.get_sound(), sound)
            self.assertTrue(channel.get_busy())

            # It plays out on its own
            start = pygame.time.get_ticks()
            ch_stopped = False
            while pygame.time.get_ticks() - start < 100:
                if not channel.get_busy():
                    ch_stopped = True
                    break
                pygame.time.wait(1)
            self.assertTrue(ch_stopped)

            # loops extends the duration
            sound.play(loops=-1)
            pygame.time.wait(30)  # 3x duration
            self.assertGreater(
                sound.get_num_channels(), 0, "looping sound should still play"
            )
            sound.stop()

            # maxtime halts playback
            channel = sound.play(loops=-1, maxtime=50)
            start = pygame.time.get_ticks()
            while channel.get_busy() and pygame.time.get_ticks() - start < 200:
                pygame.time.wait(1)
            self.assertFalse(channel.get_busy(), "maxtime should have halted playback")

            # fade_ms is accepted and playback still begins
            channel = sound.play(fade_ms=20)
            self.assertIsInstance(channel, mixer.Channel)
        finally:
            sound.stop()

    def test_volume__while_playing(self):
        """Ensure a Sound's volume can be set and read back while playing."""
        sound = get_fake_sound_duration(200)
        sound.set_volume(0.5)

        sound.play(loops=-1)
        try:
            self.assertAlmostEqual(sound.get_volume(), 0.5, places=2)
            sound.set_volume(0.25)
            self.assertAlmostEqual(sound.get_volume(), 0.25, places=2)
        finally:
            sound.stop()

    def test_set_volume(self):
        """Ensure a sound's volume can be set."""
        try:
            float_delta = 1.0 / 128  # SDL volume range is 0 to 128
            filename = example_path(os.path.join("data", "house_lo.wav"))
            sound = mixer.Sound(file=filename)
            current_volume = sound.get_volume()

            # (volume_set_value : expected_volume)
            volumes = (
                (-1, current_volume),  # value < 0 won't change volume
                (0, 0.0),
                (0.01, 0.01),
                (0.1, 0.1),
                (0.5, 0.5),
                (0.9, 0.9),
                (0.99, 0.99),
                (1, 1.0),
                (1.1, 1.0),
                (2.0, 1.0),
            )

            for volume_set_value, expected_volume in volumes:
                sound.set_volume(volume_set_value)

                self.assertAlmostEqual(
                    sound.get_volume(), expected_volume, delta=float_delta
                )
        finally:
            pygame.mixer.quit()
            with self.assertRaisesRegex(pygame.error, "mixer not initialized"):
                sound.set_volume(1)

    def test_stop(self):
        """Ensure stop can be called while not playing a sound."""
        try:
            expected_channels = 0
            filename = example_path(os.path.join("data", "house_lo.wav"))
            sound = mixer.Sound(file=filename)

            sound.stop()

            self.assertEqual(sound.get_num_channels(), expected_channels)
        finally:
            pygame.mixer.quit()
            with self.assertRaisesRegex(pygame.error, "mixer not initialized"):
                sound.stop()

    def test_stop__while_playing(self):
        """Ensure stop halts a playing sound on all of its channels."""
        sound = get_fake_sound_duration(200)

        try:
            sound.play(loops=-1)
            sound.play(loops=-1)
            self.assertEqual(sound.get_num_channels(), 2)

            sound.stop()
            self.assertEqual(sound.get_num_channels(), 0)
        finally:
            sound.stop()

    def test_stop__discards_queue(self):
        """Sound.stop() discards a queued Sound rather than advancing to it."""
        playing = get_fake_sound_duration(10)
        queued = get_fake_sound_duration(300)
        ch = mixer.Channel(0)

        try:
            ch.play(playing, loops=-1)  # loop so it can't end on its own
            ch.queue(queued)

            playing.stop()
            self.assertIsNone(
                ch.get_sound(),
                "Sound.stop() should not advance to the queued sound",
            )
        finally:
            ch.stop()

    def test_fadeout__keeps_queue(self):
        """Sound.fadeout() lets the queued Sound play once the fade completes."""
        playing = get_fake_sound_duration(10)
        queued = get_fake_sound_duration(300)
        ch = mixer.Channel(0)

        try:
            ch.play(playing, loops=-1)  # loop so it can't end on its own
            ch.queue(queued)

            playing.fadeout(10)
            advanced = False
            start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start < 200:
                pygame.time.wait(1)
                if ch.get_sound() == queued:
                    advanced = True
                    break
            self.assertTrue(
                advanced, "Sound.fadeout() should let the queued sound play"
            )
        finally:
            ch.stop()

    def test_get_raw(self):
        """Ensure get_raw returns the correct bytestring."""
        try:
            samples = b"abcdefgh"  # keep byte size a multiple of 4
            snd = mixer.Sound(buffer=samples)

            raw = snd.get_raw()

            self.assertIsInstance(raw, bytes)
            self.assertEqual(raw, samples)
        finally:
            pygame.mixer.quit()
            with self.assertRaisesRegex(pygame.error, "mixer not initialized"):
                snd.get_raw()

    def test_correct_subclassing(self):
        class CorrectSublass(mixer.Sound):
            def __init__(self, file):
                super().__init__(file=file)

        filename = example_path(os.path.join("data", "house_lo.wav"))
        correct = CorrectSublass(filename)

        try:
            correct.get_volume()
        except Exception:
            self.fail("This should not raise an exception.")

        channel = mixer.Channel(0)
        try:
            channel.play(correct)
        except Exception:
            self.fail("This should not raise an exception.")

        self.assertIsInstance(channel.get_sound(), CorrectSublass)
        self.assertIs(channel.get_sound(), correct)

        channel.stop()

    def test_incorrect_subclassing(self):
        class IncorrectSuclass(mixer.Sound):
            def __init__(self):
                pass

        incorrect = IncorrectSuclass()

        self.assertRaises(RuntimeError, incorrect.get_volume)

    def test_snd_copy(self):
        class SubSound(mixer.Sound):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        mixer.init()

        filenames = [
            "house_lo.ogg",
            "house_lo.wav",
            "house_lo.flac",
            "house_lo.opus",
            "surfonasinewave.xm",
        ]
        old_volumes = [0.1, 0.2, 0.5, 0.7, 1.0]
        new_volumes = [0.2, 0.3, 0.7, 1.0, 0.1]
        if pygame.mixer.get_sdl_mixer_version() >= (2, 6, 0):
            filenames.append("house_lo.mp3")
            old_volumes.append(0.9)
            new_volumes.append(0.5)

        for f, old_vol, new_vol in zip(filenames, old_volumes, new_volumes):
            filename = example_path(os.path.join("data", f))
            try:
                sound = mixer.Sound(file=filename)
                sound.set_volume(old_vol)
            except pygame.error:
                continue
            sound_copy = sound.copy()
            self.assertEqual(sound.get_length(), sound_copy.get_length())
            self.assertEqual(sound.get_num_channels(), sound_copy.get_num_channels())
            self.assertEqual(sound.get_volume(), sound_copy.get_volume())
            self.assertEqual(sound.get_raw(), sound_copy.get_raw())

            sound.set_volume(new_vol)
            self.assertNotEqual(sound.get_volume(), sound_copy.get_volume())

            del sound

            # Test on the copy for playable sounds
            channel = sound_copy.play()
            if channel is None:
                continue
            self.assertTrue(channel.get_busy())
            sound_copy.stop()
            self.assertFalse(channel.get_busy())
            sound_copy.play()
            self.assertEqual(sound_copy.get_num_channels(), 1)

        # Test __copy__
        for f, old_vol, new_vol in zip(filenames, old_volumes, new_volumes):
            filename = example_path(os.path.join("data", f))
            try:
                sound = mixer.Sound(file=filename)
                sound.set_volume(old_vol)
            except pygame.error:
                continue
            sound_copy = copy.copy(sound)
            self.assertEqual(sound.get_length(), sound_copy.get_length())
            self.assertEqual(sound.get_num_channels(), sound_copy.get_num_channels())
            self.assertEqual(sound.get_volume(), sound_copy.get_volume())
            self.assertEqual(sound.get_raw(), sound_copy.get_raw())

            sound.set_volume(new_vol)
            self.assertNotEqual(sound.get_volume(), sound_copy.get_volume())

            del sound

            # Test on the copy for playable sounds
            channel = sound_copy.play()
            if channel is None:
                continue
            self.assertTrue(channel.get_busy())
            sound_copy.stop()
            self.assertFalse(channel.get_busy())
            sound_copy.play()
            self.assertEqual(sound_copy.get_num_channels(), 1)

        # Test copying a subclass of Sound
        for f, old_vol, new_vol in zip(filenames, old_volumes, new_volumes):
            filename = example_path(os.path.join("data", f))
            try:
                sound = SubSound(file=filename)
                sound.set_volume(old_vol)
            except pygame.error:
                continue
            sound_copy = sound.copy()
            self.assertIsInstance(sound_copy, SubSound)
            self.assertEqual(sound.get_length(), sound_copy.get_length())
            self.assertEqual(sound.get_num_channels(), sound_copy.get_num_channels())
            self.assertEqual(sound.get_volume(), sound_copy.get_volume())
            self.assertEqual(sound.get_raw(), sound_copy.get_raw())

            sound.set_volume(new_vol)
            self.assertNotEqual(sound.get_volume(), sound_copy.get_volume())

            del sound

            # Test on the copy for playable sounds
            channel = sound_copy.play()
            if channel is None:
                continue
            self.assertTrue(channel.get_busy())
            sound_copy.stop()
            self.assertFalse(channel.get_busy())
            sound_copy.play()
            self.assertEqual(sound_copy.get_num_channels(), 1)


##################################### MAIN #####################################

if __name__ == "__main__":
    unittest.main()
