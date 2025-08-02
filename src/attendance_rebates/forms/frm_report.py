"""ReportFrame for Phoenix attendance rebates."""
import tkinter as tk
from tkinter import ttk
from tkinter import font as tk_font, messagebox
from clipboard import copy

from psiutils.constants import PAD
from psiutils.buttons import ButtonFrame, IconButton
from psiutils.widgets import separator_frame
from psiutils.utilities import window_resize, geometry

from config import get_config
from constants import APP_TITLE
import text
from rebate_process import RebateProcess

FRAME_TITLE = f'{APP_TITLE} - Totals'

BROUGHT_FORWARD = 'Brought forward'
CARRIED_FORWARD = 'Carried forward'

TOTAL_RECIPIENTS = 'Total recipients'
TOTAL_REBATE = 'Total rebate'

class ReportFrame():
    def __init__(self, parent: tk.Frame, report: RebateProcess) -> None:
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.report = report
        self.date_message = parent.date_message
        self.config = get_config()

        message = [
            'Process successfully completed ...',
            'Reports will be found in the directory:',
            f'\'{self.config.output_dir}\'',
        ]
        self.output_dir = '\n'.join(message)

        # tk variables

        self.show()

    def show(self) -> None:
        root = self.root
        root.geometry(geometry(self.config, __file__))
        root.transient(self.parent.root)
        root.title(FRAME_TITLE)

        root.bind('<Control-x>', self._dismiss)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)
        self.button_frame = self._button_frame(root)
        self.button_frame.grid(row=8, column=0, columnspan=9,
                               sticky=tk.EW, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        # frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        row = 0

        period_frame = self._period_frame(frame)
        period_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW)

        row += 1
        separator = separator_frame(frame, 'F2F')
        separator.grid(row=row, column=0, columnspan=3, sticky=tk.EW)

        row += 1
        label = ttk.Label(frame, text=BROUGHT_FORWARD)
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, text=self.report.f2f_bf, width=10,
                          anchor=tk.E, borderwidth=1, relief=tk.SUNKEN)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text=CARRIED_FORWARD)
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, text=self.report.f2f_cf, width=10,
                          anchor=tk.E, borderwidth=1, relief=tk.SUNKEN)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text=TOTAL_RECIPIENTS)
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, text=self.report.f2f_recipients, width=10,
                          anchor=tk.E, borderwidth=1, relief=tk.SUNKEN)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text=f'{TOTAL_REBATE} (£)')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, text=f'{self.report.f2f_total:.2f}', width=10,
                          anchor=tk.E, borderwidth=1, relief=tk.SUNKEN)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        separator = separator_frame(frame, 'BBO')
        separator.grid(row=row, column=0, columnspan=3, sticky=tk.EW)

        row += 1
        label = ttk.Label(frame, text=BROUGHT_FORWARD)
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, text=self.report.bbo_bf, width=10,
                          anchor=tk.E, borderwidth=1, relief=tk.SUNKEN)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text=CARRIED_FORWARD)
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, text=self.report.bbo_cf, width=10,
                          anchor=tk.E, borderwidth=1, relief=tk.SUNKEN)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text=TOTAL_RECIPIENTS)
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, text=self.report.bbo_recipients, width=10,
                          anchor=tk.E, borderwidth=1, relief=tk.SUNKEN)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text=f'{TOTAL_REBATE} ($)')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, text=f'{self.report.bbo_total:.2f}', width=10,
                          anchor=tk.E, borderwidth=1, relief=tk.SUNKEN)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        separator = separator_frame(frame, 'Output')
        separator.grid(row=row, column=0, columnspan=3, sticky=tk.EW)

        row += 1
        font = (tk_font.nametofont('TkDefaultFont'), 12, 'bold')
        label = ttk.Label(frame, text=self.output_dir, font=font)
        label.grid(row=row, column=0, columnspan=2, sticky=tk.EW)

        return frame

    def _period_frame(self, master) -> tk.Frame:
        frame = ttk.Frame(master)
        frame.columnconfigure(1, weight=1)

        sep = ttk.Separator(frame, orient='horizontal')
        sep.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=PAD)

        label = ttk.Label(frame, textvariable=self.date_message)
        label.config(font=('Arial', 12))
        label.grid(row=1, column=0, columnspan=2, sticky=tk.N, padx=PAD)

        sep = ttk.Separator(frame, orient='horizontal')
        sep.grid(row=2, column=0, columnspan=2, sticky=tk.EW, padx=PAD)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button('copy_clipboard', False, self._copy),
            frame.icon_button('exit', False, self._dismiss)
        ]
        frame.enable(False)
        return frame

    def _copy(self, *args) -> None:
        sep = '-' * 20
        rebate_stirling = f'{TOTAL_REBATE} (£)'
        rebate_dollars = f'{TOTAL_REBATE} ($)'
        output = [
            self.date_message.get(),
            f'{sep} F2F {sep}',
            f'{BROUGHT_FORWARD:<16} {self.report.f2f_bf:>8}',
            f'{CARRIED_FORWARD:<16} {self.report.f2f_cf:>8}',
            f'{TOTAL_RECIPIENTS:<16} {self.report.f2f_recipients:>8}',
            f'{rebate_stirling:<16} {self.report.f2f_total:>8.2f}',
            f'{sep} BBO {sep}',
            f'{BROUGHT_FORWARD:<16} {self.report.bbo_bf:>8}',
            f'{CARRIED_FORWARD:<16} {self.report.bbo_cf:>8}',
            f'{TOTAL_RECIPIENTS:<16} {self.report.bbo_recipients:>8}',
            f'{rebate_dollars:<16} {self.report.bbo_total:>8.2f}',
        ]
        copy('\n'.join(output))
        messagebox.showinfo('', 'Report copied to clipboard')

    def _dismiss(self, *args) -> None:
        self.root.destroy()
