"""Работа с путями виртуальной файловой системы."""


def normalize_path(path, current_path):
    """Преобразовать путь в список частей относительно корня VFS."""
    path = path.replace("\\", "/")

    if path.startswith("/"):
        parts = []
    else:
        parts = list(current_path)

    for part in path.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)

    return parts


def get_node(vfs, path_parts):
    """Получить объект VFS по нормализованному пути."""
    node = vfs
    for part in path_parts:
        if node["type"] != "dir":
            raise NotADirectoryError(part)
        if part not in node["children"]:
            raise FileNotFoundError(part)
        node = node["children"][part]
    return node


def resolve_path(vfs, path, current_path):
    """Нормализовать путь и найти объект VFS."""
    path_parts = normalize_path(path, current_path)
    node = get_node(vfs, path_parts)
    return path_parts, node


def format_path(path_parts):
    """Преобразовать путь VFS в строку."""
    if not path_parts:
        return "/"
    return "/" + "/".join(path_parts)