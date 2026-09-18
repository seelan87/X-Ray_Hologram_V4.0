# X-Ray Hologram V4.0 — GitHub Windows EXE Build

This package contains the GitHub Actions support files for building the uploaded notebook
`X-Ray_Hologram_V4.0 simplified.ipynb` as a Windows x64 ONEDIR executable.

## Repository layout

```text
.
├── X-Ray_Hologram_V4.0 simplified.ipynb
├── X-Ray_Hologram_V4.0_launcher.py
├── requirements-windows.txt
├── hooks/
│   └── pyi_rth_imageio_ffmpeg.py
├── scripts/
│   └── build_windows.ps1
└── .github/
    └── workflows/
        └── build-windows.yml
```

## What the launcher does

The notebook contains the complete Tkinter application in one code cell and contains an
embedded `root.mainloop()` before later patch code. The launcher reads the notebook at
runtime, suppresses only that embedded blocking `mainloop()` call, executes the complete
cell so all later patch code is installed, verifies that `root` and `app` were created,
and then starts `root.mainloop()` exactly once.

## GitHub use

Copy these files into the root of the repository that also contains the notebook.
Then run **Actions → Build Windows x64 ONEDIR - X-Ray Hologram V4.0 → Run workflow**.

A version tag such as `v4.0.0` also triggers the workflow automatically.

The workflow uploads:

`X-Ray_Hologram_V4.0-Windows-x64-ONEDIR.zip`

The ZIP contains the ONEDIR application and the original notebook beside the EXE.

## Important

The build is Windows x64 and uses Python 3.12, matching the supplied working workflow.
The application is packaged as ONEDIR rather than a single-file EXE because the project
depends on large scientific libraries and a bundled FFmpeg executable.
