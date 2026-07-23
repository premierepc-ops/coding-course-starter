"""Shared paths for SQLite databases and uploaded files.

Local dev: DATA_DIR defaults to the project root.
Railway: set DATA_DIR to a mounted volume (e.g. /data).
"""
import os

ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.abspath(
    os.environ.get("DATA_DIR")
    or os.environ.get("RAILWAY_VOLUME_MOUNT_PATH")
    or ROOT
)

os.makedirs(DATA_DIR, exist_ok=True)


def db_path(filename: str) -> str:
    return os.path.join(DATA_DIR, filename)
