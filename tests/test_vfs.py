"""Тесты загрузки VFS из ZIP."""

import unittest
import zipfile
from pathlib import Path

from src.vfs import load_vfs, compute_vfs_info


VFS_DIR = Path(__file__).resolve().parent / "vfs"


def ensure_zip(name):
    src = VFS_DIR / name
    dst = VFS_DIR / f"{name}.zip"
    if not dst.exists():
        with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zf:
            for item in sorted(src.rglob("*")):
                if item.is_file():
                    zf.write(item, item.relative_to(src).as_posix())
    return dst


class TestVFS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for n in ("minimal", "multiple", "nested"):
            ensure_zip(n)

    def test_minimal(self):
        vfs = load_vfs(VFS_DIR / "minimal.zip")
        content = vfs["children"]["hello.txt"]["content"]
        self.assertEqual(content.decode().strip(), "Hello from VFS!")

    def test_multiple(self):
        vfs = load_vfs(VFS_DIR / "multiple.zip")
        self.assertIn("readme.txt", vfs["children"])
        self.assertIn("config.ini", vfs["children"])
        self.assertIn("docs", vfs["children"])

    def test_nested(self):
        vfs = load_vfs(VFS_DIR / "nested.zip")
        node = vfs
        for f in ("level1", "level2", "level3"):
            node = node["children"][f]
        content = node["children"]["deep.txt"]["content"]
        self.assertEqual(content.decode().strip(), "Level 3 reached!")

    def test_missing(self):
        with self.assertRaises(FileNotFoundError):
            load_vfs(VFS_DIR / "missing.zip")

    def test_not_zip(self):
        with self.assertRaises(ValueError):
            load_vfs(VFS_DIR / "minimal" / "hello.txt")

    def test_info(self):
        name, h = compute_vfs_info(VFS_DIR / "minimal.zip")
        self.assertEqual(name, "minimal.zip")
        self.assertEqual(len(h), 64)


if __name__ == "__main__":
    unittest.main()