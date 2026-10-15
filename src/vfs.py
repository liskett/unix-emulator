"""Загрузка виртуальной файловой системы из ZIP-архива в память."""

import hashlib
import zipfile
from pathlib import Path


def load_vfs(zip_path):
    """Загрузить VFS из ZIP-архива в память (без распаковки на диск)."""
    path = Path(zip_path)

    if not path.exists():
        raise FileNotFoundError(f"VFS не найдена: {path}")

    if not zipfile.is_zipfile(path):
        raise ValueError(f"VFS должна быть ZIP-архивом: {path}")

    root = {"type": "dir", "owner": "root", "children": {}}

    with zipfile.ZipFile(path, "r") as archive:
        for name in archive.namelist():
            if name.endswith("/"):
                continue

            parts = name.split("/")
            node = root

            for part in parts[:-1]:
                if part not in node["children"]:
                    node["children"][part] = {
                        "type": "dir",
                        "owner": "root",
                        "children": {},
                    }
                node = node["children"][part]

            node["children"][parts[-1]] = {
                "type": "file",
                "owner": "root",
                "content": archive.read(name),
            }

    return root


def compute_vfs_info(zip_path):
    """Имя VFS и SHA-256 хеш содержимого архива."""
    path = Path(zip_path)
    data = path.read_bytes()
    return path.name, hashlib.sha256(data).hexdigest()