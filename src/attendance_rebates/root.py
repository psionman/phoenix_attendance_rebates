
"""
The main gui module for the application.
"""

import sys
import tkinter as tk

from psiutils.utilities import display_icon
from psiutils.widgets import get_styles

from constants import ICON_FILE
from module_caller import ModuleCaller

from forms.frm_main import MainFrame


class Root():
    def __init__(self) -> None:
        self.root = tk.Tk()
        root = self.root
        display_icon(root, ICON_FILE, ignore_error=True)
        root.protocol("WM_DELETE_WINDOW", root.destroy)

        get_styles()

        # TODO remove for rebuild only
        # self.base_date = datetime(2023, 8, 1)
        # print(f'Now running based on {self.base_date}')

        dlg = None
        if len(sys.argv) > 1:
            module = sys.argv[1]
            dlg = ModuleCaller(self.root, module)
            return

        if not dlg or dlg.invalid:
            MainFrame(self)

        root.mainloop()
