"""Тесты нормализации путей."""

import unittest

from src.path_utils import format_path, normalize_path


class TestPaths(unittest.TestCase):
    def test_complex_absolute(self):
        result = normalize_path(
            "/projects/student/files/../../archive/././docs", []
        )
        self.assertEqual(result, ["projects", "archive", "docs"])

    def test_relative(self):
        result = normalize_path("../shared/docs", ["home", "user"])
        self.assertEqual(result, ["home", "shared", "docs"])

    def test_current(self):
        result = normalize_path("./docs/./file", ["home"])
        self.assertEqual(result, ["home", "docs", "file"])

    def test_root_escape(self):
        result = normalize_path("/../../../home", [])
        self.assertEqual(result, ["home"])

    def test_slashes(self):
        result = normalize_path("/home///user//docs", [])
        self.assertEqual(result, ["home", "user", "docs"])

    def test_backslashes(self):
        result = normalize_path(r"\home\user\..\buddy", [])
        self.assertEqual(result, ["home", "buddy"])

    def test_format_root(self):
        self.assertEqual(format_path([]), "/")

    def test_format(self):
        self.assertEqual(format_path(["home", "docs"]), "/home/docs")


if __name__ == "__main__":
    unittest.main()