import os
import shutil
import tempfile
from pathlib import Path


def safe_copy(src: str, dst: str) -> None:
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def temporary_copy(src: str) -> str:
    """Return path to a temporary copy of src."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    shutil.copy2(src, path)
    return path
