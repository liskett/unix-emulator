"""Тесты команд rm и chown."""

import unittest
from pathlib import Path

from src.commands import execute
from src.path_utils import resolve_path
from src.vfs import load_vfs


VFS_DIR = Path(__file__).resolve().parent / "vfs"


def make_state():
    return {
        "vfs": load_vfs(VFS_DIR / "multiple.zip"),
        "cwd": [],
        "vfs_name": "multiple.zip",
        "vfs_hash": "x",
        "start_time": 0,
    }


class TestChown(unittest.TestCase):
    def setUp(self):
        self.state = make_state()

    def owner(self, path):
        _, node = resolve_path(self.state["vfs"], path, self.state["cwd"])
        return node["owner"]

    def test_file(self):
        r = execute("chown", ["tyoma", "readme.txt"], self.state)
        self.assertFalse(r.error)
        self.assertEqual(self.owner("readme.txt"), "tyoma")

    def test_dir(self):
        r = execute("chown", ["admin", "docs"], self.state)
        self.assertFalse(r.error)
        self.assertEqual(self.owner("docs"), "admin")

    def test_absolute(self):
        r = execute("chown", ["student", "/docs/info.txt"], self.state)
        self.assertFalse(r.error)
        self.assertEqual(self.owner("/docs/info.txt"), "student")

    def test_complex_path(self):
        r = execute(
            "chown", ["user", "/docs/.././readme.txt"], self.state
        )
        self.assertFalse(r.error)
        self.assertEqual(self.owner("readme.txt"), "user")

    def test_relative(self):
        self.state["cwd"] = ["docs"]
        r = execute("chown", ["teacher", "info.txt"], self.state)
        self.assertFalse(r.error)

    def test_no_args(self):
        r = execute("chown", [], self.state)
        self.assertTrue(r.error)

    def test_one_arg(self):
        r = execute("chown", ["tyoma"], self.state)
        self.assertTrue(r.error)

    def test_many_args(self):
        r = execute(
            "chown", ["tyoma", "readme.txt", "extra"], self.state
        )
        self.assertTrue(r.error)

    def test_missing(self):
        r = execute("chown", ["tyoma", "missing.txt"], self.state)
        self.assertTrue(r.error)

    def test_memory_only(self):
        execute("chown", ["tyoma", "readme.txt"], self.state)
        fresh = load_vfs(VFS_DIR / "multiple.zip")
        _, node = resolve_path(fresh, "readme.txt", [])
        self.assertEqual(node["owner"], "root")


class TestRm(unittest.TestCase):
    def setUp(self):
        self.state = make_state()

    def test_rm_file(self):
        r = execute("rm", ["readme.txt"], self.state)
        self.assertFalse(r.error)
        self.assertNotIn("readme.txt", self.state["vfs"]["children"])

    def test_rm_dir(self):
        r = execute("rm", ["docs"], self.state)
        self.assertTrue(r.error)

    def test_rm_missing(self):
        r = execute("rm", ["missing.txt"], self.state)
        self.assertTrue(r.error)

    def test_rm_complex(self):
        r = execute("rm", ["/docs/.././readme.txt"], self.state)
        self.assertFalse(r.error)
        self.assertNotIn("readme.txt", self.state["vfs"]["children"])

    def test_rm_memory_only(self):
        execute("rm", ["readme.txt"], self.state)
        fresh = load_vfs(VFS_DIR / "multiple.zip")
        self.assertIn("readme.txt", fresh["children"])


if __name__ == "__main__":
    unittest.main()