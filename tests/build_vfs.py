"""Собрать ZIP-архивы VFS из директорий tests/vfs/."""

import zipfile
from pathlib import Path


VFS_DIR = Path(__file__).resolve().parent / "vfs"


def build(source_dir, output_path):
    output_path = Path(output_path)
    if output_path.exists():
        output_path.unlink()
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in sorted(source_dir.rglob("*")):
            if item.is_file():
                archive.write(item, item.relative_to(source_dir).as_posix())
    print(f"Built {output_path}")


def main():
    for name in ("minimal", "multiple", "nested"):
        source = VFS_DIR / name
        if source.is_dir():
            build(source, VFS_DIR / f"{name}.zip")


if __name__ == "__main__":
    main()