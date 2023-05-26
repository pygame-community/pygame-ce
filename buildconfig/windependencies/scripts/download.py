import hashlib
import logging
import os
import sys
from os.path import join
from .config import DOWNLOAD,SDL2_VERSION

import requests

logger = logging.getLogger("Download")

file_urls = {
    f"SDL2-{SDL2_VERSION}":'https://github.com/libsdl-org/SDL/releases/download/release-2.26.4/SDL2-devel-2.26.4-VC.zip',
    "SDL2_image": "https://github.com/libsdl-org/SDL_image/archive/d40d6cc94e4601b4d23e9e886bbe168fda567b20.zip",
    "libpng": "https://github.com/libsdl-org/libpng/archive/999173059e2651fab2a0102eeba18748c4bd9827.zip",
    "jpeg": "https://github.com/libsdl-org/jpeg/archive/bc27d050625f126dcba73ae5b731272de1a89dc1.zip",
    "zlib": "https://github.com/libsdl-org/zlib/archive/f040d0cf7a553078a195d6c3af0ec78b14d4242e.zip",
    "libtiff": "https://github.com/libsdl-org/libtiff/archive/dad25b3f71cfd7f4fcb089a5881a31e65ae92c0a.zip",
    "libwebp": "https://github.com/libsdl-org/libwebp/archive/8333c34e62ff907112bb556aab2725164abdccfe.zip",
}

file_sha1 = {
    f"SDL2-{SDL2_VERSION}":'0dea77fd5ead8c1a2134af3fc256578327e25879',
    "SDL2_image": "c1c822c9b2971f631c98dc692f8bd61c103a7c54",
    "libpng": "b3f4c909bec45b3dc13fea95567588f0b2d75cd0",
    "jpeg": "7454c6d498fa6eea99992526dffaa0e02b760fe1",
    "zlib": "a12415bc52aac8f86e3635f1a6e08d5b33963ee9",
    "libtiff": "65f614adc2e7695c7aca2e82a2832b758e1dbdf5",
    "libwebp": "f16bbf45de8c72d3c3d5a37bccb2bb675e65baf2",
}
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
}

DOWNLOAD_CHUNK_SIZE = 65536


def check_sha1(filename, sha1_str):
    with open(filename, "rb") as f:
        buf = f.read()
    _sha1_str = hashlib.sha1(buf).hexdigest()
    return _sha1_str == sha1_str


def download_file(name):
    filename = name + ".zip"
    size_cnt = 0
    logger.info(f"Start to download '{filename}'")
    with open(join(DOWNLOAD, filename), "wb") as _file:
        with requests.get(file_urls[name], headers=headers, stream=True) as req:
            for buf in req.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                _file.write(buf)
                size_cnt += len(buf)
                logger.info(f"Received {size_cnt} bytes ('{filename}')")
    logger.info(f"Verifying hash...")
    if not check_sha1(join(DOWNLOAD, filename), file_sha1[name]):
        raise IOError(f"File is broken")
    logger.info(f"Download complete ('{filename}')")


def main():
    return_code = 0
    if not (os.path.exists(DOWNLOAD) and os.path.isdir(DOWNLOAD)):
        os.makedirs(DOWNLOAD)

    existing_files = os.listdir(DOWNLOAD)

    for name in file_urls:
        filename = name + ".zip"
        if filename in existing_files and check_sha1(
            join(DOWNLOAD, filename), file_sha1[name]
        ):
            logger.info(f"Skipping '{filename}'")
            continue

        for i in range(3):
            try:
                download_file(name)
                break
            except IOError as err:  # Catch exceptions from requests
                logger.error(err)
                logger.info("Retrying...")
        else:
            logger.error(f"Failed to download {filename}")
            return_code = 1
    if return_code:
        raise IOError("Download Failed.")
