"""Тесты команд этапа 4."""

import time
import unittest
from pathlib import Path

from src.commands import execute
from src.vfs import load_vfs


VFS_DIR = Path(__file__).resolve().parent / "vfs"


def make_state():
    return {
        "vfs": load_vfs(VFS_DIR / "multiple.zip"),
        "cwd": [],
        "vfs_name": "multiple.zip",
        "vfs_hash": "abc",
        "start_time": time.time(),
    }


class TestLs(unittest.TestCase):
    def setUp(self):
        self.state = make_state()

    def test_simple(self):
        r = execute("ls", [], self.state)
        self.assertFalse(r.error)
        self.assertIn("readme.txt", r.output)
        self.assertNotIn(".hidden.txt", r.output)

    def test_all(self):
        r = execute("ls", ["-a"], self.state)
        self.assertIn(".hidden.txt", r.output)
        self.assertIn(".", r.output)

    def test_long(self):
        r = execute("ls", ["-l"], self.state)
        self.assertIn("root", r.output)

    def test_human(self):
        r = execute("ls", ["-lh"], self.state)
        self.assertIn("B", r.output)

    def test_combined(self):
        r = execute("ls", ["-lah"], self.state)
        self.assertIn(".hidden.txt", r.output)
        self.assertIn("root", r.output)

    def test_separate(self):
        r = execute("ls", ["-l", "-a", "-h"], self.state)
        self.assertIn(".hidden.txt", r.output)

    def test_path(self):
        r = execute("ls", ["docs"], self.state)
        self.assertIn("info.txt", r.output)

    def test_absolute(self):
        r = execute("ls", ["/docs"], self.state)
        self.assertIn("info.txt", r.output)

    def test_complex_path(self):
        r = execute("ls", ["/docs/.././docs"], self.state)
        self.assertIn("info.txt", r.output)

    def test_bad_option(self):
        r = execute("ls", ["-x"], self.state)
        self.assertTrue(r.error)

    def test_many_paths(self):
        r = execute("ls", ["docs", "/docs"], self.state)
        self.assertTrue(r.error)


class TestCd(unittest.TestCase):
    def setUp(self):
        self.state = make_state()

    def test_relative(self):
        r = execute("cd", ["docs"], self.state)
        self.assertFalse(r.error)
        self.assertEqual(self.state["cwd"], ["docs"])

    def test_complex(self):
        r = execute("cd", ["/docs/.././docs"], self.state)
        self.assertFalse(r.error)
        self.assertEqual(self.state["cwd"], ["docs"])

    def test_missing(self):
        r = execute("cd", ["missing"], self.state)
        self.assertTrue(r.error)

    def test_file(self):
        r = execute("cd", ["readme.txt"], self.state)
        self.assertTrue(r.error)


class TestDateUptime(unittest.TestCase):
    def setUp(self):
        self.state = make_state()

    def test_date(self):
        r = execute("date", [], self.state)
        self.assertFalse(r.error)
        self.assertRegex(r.output, r"\d{4}-\d{2}-\d{2}")

    def test_uptime(self):
        r = execute("uptime", [], self.state)
        self.assertIn("Uptime:", r.output)


class TestWc(unittest.TestCase):
    def setUp(self):
        self.state = make_state()

    def test_wc(self):
        r = execute("wc", ["readme.txt"], self.state)
        self.assertFalse(r.error)
        self.assertIn("readme.txt", r.output)

    def test_wc_missing(self):
        r = execute("wc", ["missing.txt"], self.state)
        self.assertTrue(r.error)


if __name__ == "__main__":
    unittest.main()