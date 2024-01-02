
SDL_mixer 2.0

The latest version of this library is available from GitHub:
https://github.com/libsdl-org/SDL_mixer/releases

Due to popular demand, here is a simple multi-channel audio mixer.
It supports 8 channels of 16 bit stereo audio, plus a single channel of music. It can load FLAC, MP3, Ogg, VOC, and WAV format audio. It can also load MIDI, MOD, and Opus audio, depending on build options (see the note below for details.)

See the header file SDL_mixer.h and the examples playwave.c and playmus.c for documentation on this mixer library. This documentation is also available online at https://wiki.libsdl.org/SDL_mixer

The process of mixing MIDI files to wave output is very CPU intensive, so if playing regular WAVE files sound great, but playing MIDI files sound choppy, try using 8-bit audio, mono audio, or lower frequencies.

If you have built with FluidSynth support, you'll need to set the SDL_SOUNDFONTS environment variable to a Sound Font 2 (.sf2) file containing the musical instruments you want to use for MIDI playback.
(On some Linux distributions you can install the fluid-soundfont-gm package)

To play MIDI files using Timidity, you'll need to get a complete set of GUS patches from:
http://www.libsdl.org/projects/mixer/timidity/timidity.tar.gz
and unpack them in /usr/local/lib under UNIX, and C:\ under Win32.

This library is under the zlib license, see the file "LICENSE.txt" for details.

Note:
Support for software MIDI, MOD, and Opus are not included by default because of the size of the decode libraries, but you can get them by running external/download.sh
- When building with CMake, you can enable the appropriate SUPPORT_* options defined in CMakeLists.txt.
- When building with configure/make, you can build and install them normally and the configure script will detect and use them.
- When building with Visual Studio, you will need to build the libraries and then add the appropriate LOAD_* preprocessor define to the Visual Studio project.
- When building with Xcode, you can edit the config at the top of the project to enable them, and you will need to include the appropriate framework in your application.
- For Android, you can edit the config at the top of Android.mk to enable them.

The default MP3 support is provided using dr_mp3. SDL_mixer also supports using libmpg123: you can enable it by passing --enable-music-mp3-mpg123 to configure.
