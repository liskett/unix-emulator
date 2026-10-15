import argparse
import getpass
import socket
import sys
import tkinter as tk
from pathlib import Path
from tkinter import scrolledtext

from src.parser import parse
from src.commands import execute


def build_title():
    user = getpass.getuser()
    host = socket.gethostname()
    return f"Эмулятор - [{user}@{host}]"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Shell emulator")
    parser.add_argument("--vfs", help="Path to VFS")
    parser.add_argument("--script", help="Path to startup script")
    return parser.parse_args(argv)


def run_script(path, printer, state=None):
    """Выполнить стартовый скрипт. Ошибочные строки пропускаются."""
    try:
        with open(path, encoding="utf-8") as script:
            for raw_line in script:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue

                printer(f"$ {line}\n")
                command, args = parse(line)
                result = execute(command, args, state)

                if result.output:
                    printer(result.output + "\n", result.error)

                if result.exit:
                    return None
    except (OSError, UnicodeError) as e:
        printer(f"Ошибка чтения скрипта: {e}\n", True)
        return False
    return True

def run_headless(args):
    def printer(text, error=False):
        stream = sys.stderr if error else sys.stdout
        stream.write(text)

    print(f"VFS: {args.vfs or '(не указан)'}")
    print(f"Скрипт: {args.script or '(не указан)'}")

    if not Path(args.script).is_file():
        print(f"Ошибка: скрипт не найден: {args.script}", file=sys.stderr)
        return 1

    result = run_script(args.script, printer)
    if result is False:
        return 1
    return 0

class EmulatorApp:
    def __init__(self, root, args):
        self.root = root
        self.root.title(build_title())
        self.root.geometry("820x560")
        self._build_ui()

        self._append(f"VFS: {args.vfs or '(не указан)'}\n")
        self._append(f"Скрипт: {args.script or '(не указан)'}\n\n")

        if args.script is not None:
            if not Path(args.script).is_file():
                self._append(
                    f"Ошибка: скрипт не найден: {args.script}\n",
                    error=True,
                )
            else:
                self._run_script(args.script)

        self.entry.focus_set()

    def _build_ui(self):
        self.output = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, bg="black", fg="#d0d0d0",
            insertbackground="white", font=("Consolas", 11),
            state="disabled",
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=4, pady=(0, 4))

        tk.Label(frame, text="$", font=("Consolas", 11)).pack(side=tk.LEFT)

        self.entry = tk.Entry(frame, font=("Consolas", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))
        self.entry.bind("<Return>", self._on_enter)

    def _append(self, text, error=False):
        self.output.config(state="normal")
        if error:
            self.output.insert(tk.END, text, "error")
            self.output.tag_config("error", foreground="#ff6b6b")
        else:
            self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state="disabled")

    def _run_script(self, path):
        def printer(text, error=False):
            self._append(text, error)
        result = run_script(path, printer)
        if result is None:
            self._append("Bye.\n")
            self.root.after(200, self.root.destroy)

    def _on_enter(self, event):
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        if not line.strip():
            return

        self._append(f"$ {line}\n")
        command, args = parse(line)
        if command is None:
            return

        result = execute(command, args)
        if result.exit:
            self._append("Bye.\n")
            self.root.after(200, self.root.destroy)
            return
        if result.output:
            self._append(result.output + "\n", error=result.error)


def run_gui(args):
    root = tk.Tk()
    EmulatorApp(root, args)
    root.mainloop()
    return 0


def main():
    args = parse_args()
    if args.script is not None:
        return run_headless(args)
    return run_gui(args)


if __name__ == "__main__":
    raise SystemExit(main())