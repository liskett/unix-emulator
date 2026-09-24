class CommandResult:
    def __init__(self, output='', error=False, exit=False):
        self.output = output
        self.error = error
        self.exit = exit


def cmd_ls(args):
    """Заглушка: выводит своё имя и аргументы."""
    return CommandResult(f"ls: args={args}")


def cmd_cd(args):
    """Заглушка: выводит своё имя и аргументы."""
    return CommandResult(f"cd: args={args}")


def cmd_exit(args):
    return CommandResult(exit=True)


COMMANDS = {
    'ls': cmd_ls,
    'cd': cmd_cd,
    'exit': cmd_exit,
}


def execute(command, args):
    if command not in COMMANDS:
        return CommandResult(f"{command}: command not found", error=True)
    try:
        return COMMANDS[command](args)
    except Exception as e:
        return CommandResult(f"{command}: error: {e}", error=True)