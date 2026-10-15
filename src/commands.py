"""Команды эмулятора командной оболочки."""

import time
from datetime import datetime

from src.path_utils import format_path, get_node, resolve_path


LS_OPTIONS = {"l", "h", "a"}
SINGLE_ARG_COUNT = 1
KIB = 1024
class CommandResult:
    def __init__(self, output='', error=False, exit=False):
        self.output = output
        self.error = error
        self.exit = exit



def cmd_cd(args, state):
    if len(args) != SINGLE_ARG_COUNT:
        return CommandResult(
            "Ошибка: команда cd ожидает один аргумент", error=True
        )

    try:
        path_parts, node = resolve_path(
            state["vfs"], args[0], state["cwd"]
        )
    except FileNotFoundError:
        return CommandResult("Ошибка: каталог не найден", error=True)
    except NotADirectoryError:
        return CommandResult(
            "Ошибка: часть пути не является каталогом", error=True
        )

    if node["type"] != "dir":
        return CommandResult(
            "Ошибка: указанный путь не является каталогом", error=True
        )

    state["cwd"][:] = path_parts
    return CommandResult()



def parse_ls_arguments(args):
    options = set()
    paths = []

    for arg in args:
        if arg.startswith("-") and arg != "-":
            for opt in arg[1:]:
                if opt not in LS_OPTIONS:
                    raise ValueError(f"неизвестный ключ: -{opt}")
                options.add(opt)
        else:
            paths.append(arg)

    if len(paths) > 1:
        raise ValueError("команда ls принимает не более одного пути")

    path = paths[0] if paths else "."
    return options, path


def human_size(size):
    units = ("B", "K", "M", "G")
    value = float(size)
    i = 0
    while value >= KIB and i < len(units) - 1:
        value /= KIB
        i += 1
    if i == 0:
        return f"{int(value)}B"
    return f"{value:.1f}{units[i]}"


def node_size(node):
    if node["type"] == "file":
        return len(node["content"])
    return 0


def format_long_entry(name, node, human):
    obj_type = "d" if node["type"] == "dir" else "-"
    owner = node.get("owner", "root")
    size = node_size(node)
    size_text = human_size(size) if human else str(size)
    return f"{obj_type} {owner} {size_text:>6} {name}"


def directory_entries(vfs, node, path_parts, show_all):
    entries = list(node["children"].items())
    if not show_all:
        return [e for e in entries if not e[0].startswith(".")]
    parent = get_node(vfs, path_parts[:-1])
    return [(".", node), ("..", parent)] + entries


def format_entry(name, node, options):
    if "l" in options:
        return format_long_entry(name, node, "h" in options)
    return name


def cmd_ls(args, state):
    try:
        options, path = parse_ls_arguments(args)
    except ValueError as e:
        return CommandResult(f"Ошибка: {e}", error=True)

    try:
        path_parts, node = resolve_path(
            state["vfs"], path, state["cwd"]
        )
    except FileNotFoundError:
        return CommandResult("Ошибка: путь не найден", error=True)
    except NotADirectoryError:
        return CommandResult(
            "Ошибка: часть пути не является каталогом", error=True
        )

    if node["type"] == "file":
        return CommandResult(format_entry(path_parts[-1], node, options))

    entries = directory_entries(
        state["vfs"], node, path_parts, "a" in options
    )
    lines = [format_entry(n, c, options) for n, c in entries]
    return CommandResult("\n".join(lines))



def cmd_vfs_info(args, state):
    if args:
        return CommandResult(
            "Ошибка: команда vfs-info не принимает аргументы", error=True
        )
    name = (state or {}).get("vfs_name", "(не указан)")
    h = (state or {}).get("vfs_hash", "(не указан)")
    return CommandResult(f"Имя VFS: {name}\nSHA-256: {h}")



def cmd_date(args, state):
    if args:
        return CommandResult(
            "Ошибка: команда date не принимает аргументы", error=True
        )
    now = datetime.now().astimezone()
    return CommandResult(now.strftime("%Y-%m-%d %H:%M:%S %Z"))



def cmd_wc(args, state):
    if len(args) != SINGLE_ARG_COUNT:
        return CommandResult(
            "Ошибка: команда wc ожидает один аргумент", error=True
        )

    try:
        path_parts, node = resolve_path(
            state["vfs"], args[0], state["cwd"]
        )
    except FileNotFoundError:
        return CommandResult("Ошибка: путь не найден", error=True)
    except NotADirectoryError:
        return CommandResult(
            "Ошибка: часть пути не является каталогом", error=True
        )

    if node["type"] != "file":
        return CommandResult(
            "Ошибка: wc работает только с файлами", error=True
        )

    raw = node["content"]
    text = raw.decode("utf-8", errors="replace")
    lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    words = len(text.split())
    size = len(raw)
    return CommandResult(f"{lines} {words} {size} {path_parts[-1]}")



def cmd_uptime(args, state):
    if args:
        return CommandResult(
            "Ошибка: команда uptime не принимает аргументы", error=True
        )
    elapsed = int(time.time() - (state or {}).get("start_time", time.time()))
    h = elapsed // 3600
    m = (elapsed % 3600) // 60
    s = elapsed % 60
    return CommandResult(f"Uptime: {h}:{m:02d}:{s:02d}")



def cmd_exit(args, state):
    if args:
        return CommandResult(
            "Ошибка: команда exit не принимает аргументы", error=True
        )
    return CommandResult(exit=True)



COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "vfs-info": cmd_vfs_info,
    "date": cmd_date,
    "wc": cmd_wc,
    "uptime": cmd_uptime,
    "exit": cmd_exit,
}


def execute(command, args, state=None):
    if command not in COMMANDS:
        return CommandResult(f"{command}: command not found", error=True)
    if state is None:
        state = {
            "vfs": {"type": "dir", "owner": "root", "children": {}},
            "cwd": [],
            "vfs_name": "(не указан)",
            "vfs_hash": "(не указан)",
            "start_time": time.time(),
        }
    try:
        return COMMANDS[command](args, state)
    except Exception as e:
        return CommandResult(f"{command}: error: {e}", error=True)


def make_prompt(state):
    """Приглашение командной строки (используется в headless)."""
    return f"{state.get('vfs_name', 'vfs')}:{format_path(state['cwd'])}$"