import socket
import getpass
import tkinter as tk
from tkinter import scrolledtext

from parser import parse
from commands import execute


def build_title():
    user = getpass.getuser()
    host = socket.gethostname()
    return f"Эмулятор - [{user}@{host}]"


class EmulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title(build_title())
        self.root.geometry('820x560')

        self._build_ui()
        self._print_banner()
        self.entry.focus_set()

    def _build_ui(self):
        self.output = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, bg='black', fg='#d0d0d0',
            insertbackground='white', font=('Consolas', 11), state='disabled'
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=4, pady=(0, 4))

        self.prompt_label = tk.Label(frame, text='$', font=('Consolas', 11))
        self.prompt_label.pack(side=tk.LEFT)

        self.entry = tk.Entry(frame, font=('Consolas', 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))
        self.entry.bind('<Return>', self._on_enter)

    def _print_banner(self):
        self._append("Welcome to emulator (stage 1: REPL prototype).\n")
        self._append("Type 'exit' to quit.\n\n")

    def _append(self, text, error=False):
        self.output.config(state='normal')
        if error:
            self.output.insert(tk.END, text, 'error')
            self.output.tag_config('error', foreground='#ff6b6b')
        else:
            self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.config(state='disabled')

    def _on_enter(self, event):
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self._append(f"$ {line}\n")
        self._process_line(line)

    def _process_line(self, line):
        command, args = parse(line)
        if command is None:
            return
        result = execute(command, args)
        if result.exit:
            self._append("Bye.\n")
            self.root.after(200, self.root.destroy)
            return
        if result.output:
            self._append(result.output + '\n', error=result.error)


def main():
    root = tk.Tk()
    EmulatorApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()