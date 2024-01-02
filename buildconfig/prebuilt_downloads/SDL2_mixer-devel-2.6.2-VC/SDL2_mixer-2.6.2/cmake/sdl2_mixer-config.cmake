# SDL2_mixer CMake configuration file:
# This file is meant to be placed in a cmake subfolder of SDL2_mixer-devel-2.x.y-VC

include(FeatureSummary)
set_package_properties(SDL2_mixer PROPERTIES
    URL "https://www.libsdl.org/projects/SDL_mixer/"
    DESCRIPTION "SDL_mixer is a sample multi-channel audio mixer library"
)

cmake_minimum_required(VERSION 3.0)

set(SDL2_mixer_FOUND                TRUE)

set(SDL2MIXER_VENDORED              TRUE)

set(SDL2MIXER_CMD                   FALSE)

set(SDL2MIXER_FLAC_LIBFLAC          FALSE)
set(SDL2MIXER_FLAC_DRFLAC           TRUE)

set(SDL2MIXER_MOD                   TRUE)
set(SDL2MIXER_MOD_MODPLUG           TRUE)
set(SDL2MIXER_MOD_XMP               FALSE)
set(SDL2MIXER_MOD_XMP_LITE          FALSE)

set(SDL2MIXER_MP3                   TRUE)
set(SDL2MIXER_MP3_DRMP3             TRUE)
set(SDL2MIXER_MP3_MPG123            FALSE)

set(SDL2MIXER_MIDI                  TRUE)
set(SDL2MIXER_MIDI_FLUIDSYNTH       FALSE)
set(SDL2MIXER_MIDI_NATIVE           TRUE)
set(SDL2MIXER_MIDI_TIMIDITY         TRUE)

set(SDL2MIXER_OPUS                  TRUE)

set(SDL2MIXER_VORBIS                STB)
set(SDL2MIXER_VORBIS_STB            TRUE)
set(SDL2MIXER_VORBIS_TREMOR         FALSE)
set(SDL2MIXER_VORBIS_VORBISFILE     FALSE)

set(SDL2MIXER_WAVE                  TRUE)

if(CMAKE_SIZEOF_VOID_P STREQUAL "4")
    set(_sdl_arch_subdir "x86")
elseif(CMAKE_SIZEOF_VOID_P STREQUAL "8")
    set(_sdl_arch_subdir "x64")
else()
    unset(_sdl_arch_subdir)
    set(SDL2_mixer_FOUND FALSE)
    return()
endif()

set(_sdl2mixer_incdir       "${CMAKE_CURRENT_LIST_DIR}/../include")
set(_sdl2mixer_library      "${CMAKE_CURRENT_LIST_DIR}/../lib/${_sdl_arch_subdir}/SDL2_mixer.lib")
set(_sdl2mixer_dll          "${CMAKE_CURRENT_LIST_DIR}/../lib/${_sdl_arch_subdir}/SDL2_mixer.dll")

# All targets are created, even when some might not be requested though COMPONENTS.
# This is done for compatibility with CMake generated SDL2_mixer-target.cmake files.

if(NOT TARGET SDL2_mixer::SDL2_mixer)
    add_library(SDL2_mixer::SDL2_mixer SHARED IMPORTED)
    set_target_properties(SDL2_mixer::SDL2_mixer
        PROPERTIES
            INTERFACE_INCLUDE_DIRECTORIES "${_sdl2mixer_incdir}"
            IMPORTED_IMPLIB "${_sdl2mixer_library}"
            IMPORTED_LOCATION "${_sdl2mixer_dll}"
            COMPATIBLE_INTERFACE_BOOL "SDL2_SHARED"
            INTERFACE_SDL2_SHARED "ON"
    )
endif()

unset(_sdl_arch_subdir)
unset(_sdl2mixer_incdir)
unset(_sdl2mixer_library)
unset(_sdl2mixer_dll)
