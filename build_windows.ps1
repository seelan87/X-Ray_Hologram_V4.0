# Local Windows PowerShell build using the same inputs as GitHub Actions.
$ErrorActionPreference = "Stop"

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-windows.txt
python -m pip install --upgrade "pyinstaller>=6.11,<7"

python -m py_compile X-Ray_Hologram_V4.0_launcher.py
python -m py_compile hooks/pyi_rth_imageio_ffmpeg.py

Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

python -m PyInstaller `
  --clean `
  --noconfirm `
  --onedir `
  --windowed `
  --name "X-Ray_Hologram_V4.0" `
  --runtime-hook "hooks/pyi_rth_imageio_ffmpeg.py" `
  --collect-all h5py `
  --collect-all numpy `
  --collect-all scipy `
  --collect-all pandas `
  --collect-all matplotlib `
  --collect-all skimage `
  --collect-all imageio `
  --collect-all imageio_ffmpeg `
  --collect-all PIL `
  --hidden-import h5py `
  --hidden-import imageio `
  --hidden-import imageio.v2 `
  --hidden-import imageio_ffmpeg `
  --hidden-import matplotlib.backends.backend_tkagg `
  --hidden-import PIL._tkinter_finder `
  "X-Ray_Hologram_V4.0_launcher.py"

$appDir = (Get-ChildItem -LiteralPath "dist" -Recurse -File -Filter "X-Ray_Hologram_V4.0.exe" | Select-Object -First 1).Directory.FullName
if (!$appDir) {
  throw "EXE was not produced."
}

Copy-Item -LiteralPath "X-Ray_Hologram_V4.0 simplified.ipynb" -Destination (Join-Path $appDir "X-Ray_Hologram_V4.0 simplified.ipynb") -Force

$zip = "X-Ray_Hologram_V4.0-Windows-x64-ONEDIR.zip"
Compress-Archive -Path (Join-Path $appDir "*") -DestinationPath $zip -Force
Write-Host "Build complete: $zip"
