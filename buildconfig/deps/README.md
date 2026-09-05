# Dependency Builds

The `base/` sub-directory contains the scripts used to build the dependencies (direct and transitive) required by pygame-ce on Linux, macOS, and Windows. These are organized by library. Most dependency sub-folders are structured as:

```text
<dependency>/
├── build-<dependency>.sh
└── <dependency>.sha512
```

The `build-*.sh` scripts download and build the dependency, while the checksum files are used to verify the downloaded source archives.

## Linux (Manylinux) Wheels

The basic idea is that we build dependencies in a manylinux docker image and use these images to do builds on CI so that they don't get rebuilt for every CI run. After a successful build, the resulting base images are uploaded to [GitHub Packages](https://github.com/orgs/pygame-community/packages).

## macOS and Windows

The `mac/` directory and `win/` subdirectories have scripts that reuse dependency scripts from `base/` to make macOS and Windows builds respectively. The main difference here is that we don't make use of docker on these platforms, the built artifacts simply get stored in github cache once built.

`mac/build_mac_deps.sh` is designed to be run on a Virtual Machine that can be destroyed. It deletes some homebrew files, and messes with /usr/local/. It tries to work as far back as Mac OSX 10.11, for x64 and arm64 architectures.

Warning: *do not run on your own machine*.

If there needs to be separate configure options between linux, mac and windows
then something like the following can be used.

```bash
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    export FLUIDSYNTH_EXTRA_PLAT_FLAGS="-Denable-alsa=NO -Denable-systemd=NO"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # We don't need fluidsynth framework on mac builds
    export FLUIDSYNTH_EXTRA_PLAT_FLAGS="-Denable-framework=NO"
elif [[ -n "$WIN_ARCH" ]]; then
    # statically link against libstdc++
    export FLUIDSYNTH_EXTRA_PLAT_FLAGS="-DCMAKE_CXX_FLAGS=-static-libstdc++"
fi
```

## TODO

Maybe these need adding?

* Vulkan, via Mesa?
