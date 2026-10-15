class CommandResult:
    def __init__(self, output='', error=False, exit=False):
        self.output = output
        self.error = error
        self.exit = exit


def cmd_ls(args,state):
    """Заглушка: выводит своё имя и аргументы."""
    return CommandResult(f"ls: args={args}")


def cmd_cd(args,state):
    """Заглушка: выводит своё имя и аргументы."""
    return CommandResult(f"cd: args={args}")

def cmd_vfs_info(args, state):
    """Информация о загруженной VFS."""
    if args:
        return CommandResult(
            "vfs-info: не принимает аргументы", error=True
        )

    name = (state or {}).get("vfs_name", "(не указан)")
    h = (state or {}).get("vfs_hash", "(не указан)")
    return CommandResult(f"Имя VFS: {name}\nSHA-256: {h}")

def cmd_exit(args,state):
    return CommandResult(exit=True)


COMMANDS = {
    'ls': cmd_ls,
    'cd': cmd_cd,
    "vfs-info": cmd_vfs_info,
    'exit': cmd_exit,
}


def execute(command, args, state=None):
    if command not in COMMANDS:
        return CommandResult(f"{command}: command not found", error=True)
    try:
        return COMMANDS[command](args,state)
    except Exception as e:
        return CommandResult(f"{command}: error: {e}", error=True)