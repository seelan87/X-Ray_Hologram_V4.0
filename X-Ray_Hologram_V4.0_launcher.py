"""
Windows launcher for the X-Ray Hologram Tkinter application.

The uploaded notebook contains the complete application in its code cell.
It also contains an embedded `root.mainloop()` before later patch functions.
For a packaged EXE we execute the complete cell with only that blocking
mainloop call suppressed, then start mainloop after all notebook patches have
been installed.
"""

from __future__ import annotations

import json
import os
import re
import sys
import traceback
from pathlib import Path
import tkinter.messagebox as messagebox


NOTEBOOK_NAME = "X-Ray_Hologram_V4.0 simplified.ipynb"


def application_dir() -> Path:
    """Return the directory containing the EXE when frozen, or this script."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def notebook_path() -> Path:
    path = application_dir() / NOTEBOOK_NAME
    if not path.exists():
        raise FileNotFoundError(
            f"Required source notebook was not found:\n{path}\n\n"
            "Keep the notebook beside the EXE."
        )
    return path


def load_application_source(path: Path | str) -> str:
    """Read the notebook and return its code after neutralizing embedded mainloop."""
    # GitHub Actions/PyInstaller may pass this as a plain Windows string.
    # Normalize it immediately so pathlib methods such as .open() always work.
    path = Path(path)
    with path.open("r", encoding="utf-8") as fh:
        book = json.load(fh)

    cells = book.get("cells", [])
    code_cells = [
        "".join(cell.get("source", []))
        for cell in cells
        if cell.get("cell_type") == "code"
    ]
    if not code_cells:
        raise RuntimeError("No Python code cell was found in the application notebook.")

    # The supplied notebook contains one complete application code cell.
    source = "\n\n".join(code_cells)

    # Do not remove root/app creation. We only prevent the embedded blocking
    # mainloop from stopping execution before the later notebook patch code.
    mainloop_pattern = re.compile(r"(?m)^(?P<indent>[ \t]*)root\.mainloop\(\)[ \t]*$")
    matches = list(mainloop_pattern.finditer(source))
    if not matches:
        raise RuntimeError(
            "The application notebook does not contain the expected "
            "`root.mainloop()` call."
        )

    source = mainloop_pattern.sub(
        lambda m: f"{m.group('indent')}# PACKAGED-LAUNCHER: embedded mainloop suppressed",
        source,
    )

    return source


def write_error_log(exc: BaseException) -> Path:
    log_path = application_dir() / "X-Ray_Hologram_error.log"
    try:
        log_path.write_text(
            "X-Ray Hologram startup failure\n"
            "================================\n\n"
            + "".join(traceback.format_exception(exc)),
            encoding="utf-8",
        )
    except Exception:
        pass
    return log_path


def show_startup_error(exc: BaseException) -> None:
    log_path = write_error_log(exc)
    try:
        messagebox.showerror(
            "X-Ray Hologram - Startup Error",
            f"{type(exc).__name__}: {exc}\n\n"
            f"Details were written to:\n{log_path}",
        )
    except Exception:
        pass


def main() -> None:
    notebook = notebook_path()
    source = load_application_source(notebook)

    namespace = {
        "__name__": "__xray_hologram_runtime__",
        "__file__": str(notebook),
        "__package__": None,
        "__cached__": None,
    }

    exec(compile(source, str(notebook), "exec"), namespace, namespace)

    root = namespace.get("root")
    app = namespace.get("app")

    if root is None or app is None:
        raise RuntimeError(
            "The notebook did not create the expected `root` and `app` objects."
        )

    # The notebook's patches have now all executed. Start the GUI only once.
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        show_startup_error(exc)
        raise
