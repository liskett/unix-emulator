def parse(line: str):
    """Разбивает ввод на команду и аргументы по пробелам."""
    parts = line.split()
    if not parts:
        return None, []
    return parts[0], parts[1:]
