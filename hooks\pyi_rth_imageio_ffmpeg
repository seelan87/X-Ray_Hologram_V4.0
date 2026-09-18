"""
PyInstaller runtime hook for imageio-ffmpeg.

The ImageIO-FFmpeg package contains a Windows FFmpeg binary. PyInstaller
collects the package with --collect-all; this hook makes the bundled executable
explicitly available to imageio-ffmpeg before the first video export.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _set_bundled_ffmpeg() -> None:
    roots = []

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        roots.append(Path(meipass))

    roots.append(Path(sys.executable).resolve().parent)

    candidates = []
    for root in roots:
        candidates.extend(
            [
                root / "imageio_ffmpeg" / "binaries",
                root / "_internal" / "imageio_ffmpeg" / "binaries",
            ]
        )

    for directory in candidates:
        if not directory.is_dir():
            continue
        for exe in sorted(directory.glob("ffmpeg*.exe")):
            os.environ["IMAGEIO_FFMPEG_EXE"] = str(exe)
            return


_set_bundled_ffmpeg()
