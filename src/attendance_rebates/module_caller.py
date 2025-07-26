# import sys
# import tkinter as tk

from config import get_config
from session import Session
from forms.frm_rebate import RebateFrame
from forms.frm_emails import EmailFrame
from forms.frm_config import ConfigFrame
from forms.frm_verify import VerifyFrame


class ModuleCaller():
    def __init__(self, root, module) -> None:
        modules = {
            'rebate': self._rebate,
            'email': self._email,
            'config': self._config,
            'verify': self._verify,
            }

        self.invalid = False
        if module == '-h':
            print(modules.keys())
            self.invalid = True
            return

        if module not in modules:
            print(f'Invalid module name: {module}')
            self.invalid = True
            return

        self.root = root
        self.session = Session()
        self.config = get_config()
        modules[module]()
        self.root.destroy()
        return

    def _rebate(self) -> None:
        dlg = RebateFrame(self)
        self.root.wait_window(dlg.root)

    def _email(self) -> None:
        dlg = EmailFrame(self)
        self.root.wait_window(dlg.root)

    def _config(self) -> None:
        dlg = ConfigFrame(self)
        self.root.wait_window(dlg.root)

    def _verify(self) -> None:
        dlg = VerifyFrame(self)
        self.root.wait_window(dlg.root)
