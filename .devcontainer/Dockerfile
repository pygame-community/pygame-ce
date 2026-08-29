FROM python:3.13-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=120 \
    PATH="/home/vscode/.local/bin:${PATH}"

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update \
    && apt-get upgrade --no-install-recommends -y \
    && apt-get install --no-install-recommends -y \
        ipython3 \
        git \
        ripgrep \
        less \
        ffmpeg \
        sudo \
        libsdl2-dev \
        libsdl2-mixer-dev \
        libsdl2-image-dev \
        libsdl2-ttf-dev \
        libsdl2-gfx-dev \
        libportmidi-dev \
        libxcb-xtest0-dev \
        libgl1 \
        libglib2.0-0 \
        libx11-6 \
        libxext6 \
        libxrender1 \
        libpulse0 \
        openssh-client \
        build-essential \
        make \
        pkg-config \
        cmake \
        clang \
        ninja-build \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --shell /bin/bash --uid 1000 vscode

WORKDIR /workspaces/pygame-ce

COPY pyproject.toml README.rst /tmp/pygame-ce/

# COPY src /tmp/pygame-ce/src
# RUN python -m pip install --no-cache-dir /tmp/pygame-ce

USER vscode