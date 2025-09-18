
import tkinter as tk
from tkinter import ttk, messagebox

from psiutils. buttons import ButtonFrame, IconButton
from psiutils.widgets import clickable_widget
from psiutils.utilities import window_resize, geometry
from psiutils.constants import PAD

from config import get_config
from session import Session
from verify import verification
import text

TITLE = 'Verify a player\'s data'
TEST_EBU = '492064'


class VerifyFrame():
    def __init__(self, parent):
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.ebu = tk.StringVar(value=TEST_EBU)
        self.session = Session()
        self.config = get_config()

        self.show()
        self._got_focus()

    def show(self):
        root = self.root
        root.geometry(geometry(self.config, __file__))
        root.transient(self.parent.root)
        root.title(TITLE)

        root.bind('<Control-x>', self._dismiss)
        root.bind('<Control-v>', self._verify_files)
        self.root.bind("<FocusIn>", self._got_focus)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ttk.Frame(master)

        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)

        label = ttk.Label(frame, text='Ebu number')
        label.grid(row=0, column=0, sticky=tk.E, padx=PAD)
        entry = ttk.Entry(frame,  textvariable=self.ebu)
        entry.grid(row=0, column=1, sticky=tk.EW)

        self.text = tk.Text(frame, height=20)
        self.text.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.text.bind('<Key>', lambda e: 'break')

        button_frame = self._button_frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2,
                          sticky=tk.EW, padx=PAD, pady=PAD)
        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            IconButton(frame, text.VERIFY, 'done', self._verify_files),
            frame.icon_button('exit', self._dismiss)
        ]
        return frame

    def _verify_files(self, *args):
        result = verification(
            self.session,
            self.ebu.get())

        if result and isinstance(result, list):
            self.text.delete('0.0', tk.END)
            self.text.insert('1.0', '\n'.join(result))
            messagebox.showinfo(
                'Verify files',
                'Files verified',
                parent=self.root)
        elif result and isinstance(result, str):
            messagebox.showerror(
                'Verify files',
                result,
                parent=self.root)
        else:
            messagebox.showerror(
                'Verify files',
                'Files not verified - see terminal',
                parent=self.root)

    def _got_focus(self, *args) -> None:
        self.config = get_config()

    def _dismiss(self, *args):
        self.root.destroy()
