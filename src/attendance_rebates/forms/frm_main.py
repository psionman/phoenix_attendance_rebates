import tkinter as tk
from tkinter import ttk

from psiutils.widgets import clickable_widget
from psiutils.buttons import IconButton
from psiutils.constants import PAD
from psiutils.utilities import window_resize, geometry

from session import Session
from config import get_config

import text
from forms.frm_emails import EmailFrame
from forms.frm_rebate import RebateFrame
from forms.frm_verify import VerifyFrame
from menu import MainMenu


class MainFrame():
    def __init__(self, parent):
        self.parent = parent
        self.root = self.parent.root
        self.config = get_config()
        self.session = Session()
        self.show()

    def show(self):
        root = self.root
        root.geometry(geometry(self.config, __file__))
        root.title(text.TITLE)
        root.bind('<Control-r>', self._rebate)
        root.bind('<Control-e>', self._emails)
        root.bind('<Control-v>', self._verify)
        root.bind('<Control-x>', self._dismiss)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        root.rowconfigure(1, weight=1)
        root.columnconfigure(0, weight=1)

        main_menu = MainMenu(self)
        main_menu.create()

        button_frame = self._button_frame(self.root)
        button_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

    def _button_frame(self, container: tk.Frame) -> tk.Frame:
        frame = ttk.Frame(container)
        for frame_row in range(5):
            frame.rowconfigure(frame_row, weight=1)
        frame.columnconfigure(0, weight=1)

        row = 0
        button = IconButton(
            frame, 'Rebate report', 'report', False, self._rebate)
        button.grid(row=row, column=0)
        clickable_widget(button)

        row += 1
        button = IconButton(frame, 'Email files', 'send', False, self._emails)
        button.grid(row=row, column=0)
        clickable_widget(button)

        row += 1
        button = IconButton(frame, 'Verify', 'done', False, self._verify)
        button.grid(row=row, column=0)
        clickable_widget(button)

        row += 1
        button = IconButton(frame, text.CLOSE, 'cancel', False, self._dismiss)
        button.grid(row=row, column=0)
        clickable_widget(button)

        return frame

    def _rebate(self, *args):
        dlg = RebateFrame(self)
        self.root.wait_window(dlg.root)

    def _emails(self, *args):
        dlg = EmailFrame(self)
        self.root.wait_window(dlg.root)

    def _verify(self, *args):
        VerifyFrame(self)

    def _dismiss(self, *args):
        self.root.destroy()
