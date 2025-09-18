
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from datetime import datetime

from psiutils.widgets import separator_frame
from psiutils. buttons import ButtonFrame
from psiutils.utilities import window_resize, geometry
from psiutils.constants import PAD
from psiutils import messagebox

from attendance_rebates.config import get_config
from attendance_rebates.session import Session
from attendance_rebates.common import check_files, check_dirs
from attendance_rebates.rebate_process import RebateProcess, Context


from attendance_rebates.menu import MainMenu
from attendance_rebates.forms.frm_report import ReportFrame

TITLE = 'Rebate reports'


class RebateFrame():
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(parent.root)
        session = Session()
        self.session = session
        config = get_config()
        self.config = config

        # Needed for config
        self.year_start = session.year_start

        # tk variables
        self.year_start = tk.StringVar()
        self.date_message = tk.StringVar()
        self.payment_months = tk.StringVar()
        self.rebate_f2f = tk.StringVar()
        self.rebate_bbo = tk.StringVar()
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.membership_file = tk.StringVar()
        self.file_message = tk.StringVar()
        self.members_text = tk.StringVar()
        self.f2f_input_file = tk.StringVar()
        self.f2f_att_report = tk.StringVar()
        self.f2f_rebate_file = tk.StringVar()
        self.bbo_rebate_file = tk.StringVar()
        self.bbo_input_file = tk.StringVar()
        self.bbo_att_report = tk.StringVar()
        self.cf_input_file = tk.StringVar()
        self.cf_output_file = tk.StringVar()

        self._show()
        self._got_focus()

    def _show(self) -> None:
        root = self.root
        root.geometry(geometry(self.config, __file__))
        root.transient(self.parent.root)
        root.title(TITLE)

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        root.bind('<Control-x>', self._dismiss)
        root.bind('<Control-p>', self._create_rebate_files)
        self.root.bind("<FocusIn>", self._got_focus)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        main_menu = MainMenu(self)
        main_menu.create()

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(self.root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, container: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(container)
        frame.grid(row=0, column=0, sticky=tk.NSEW)

        frame.rowconfigure(3, weight=1)
        frame.columnconfigure(0, weight=1)  # Essential

        header = ttk.Label(frame, text=TITLE, font=('Arial', 16))
        header.grid(row=0, column=0, padx=PAD)

        information_frame = self._info_frame(frame)
        information_frame.grid(row=1, column=0, sticky=tk.EW, padx=PAD)

        period_frame = self._period_frame(frame)
        period_frame.grid(row=2, column=0, sticky=tk.EW)

        files_frame = self._files_frame(frame)
        files_frame.grid(row=3, column=0, sticky=tk.NSEW)

        button_frame = self._button_frame(frame)
        button_frame.grid(row=4, column=0, sticky=tk.EW, padx=PAD, pady=PAD)

        return frame

    def _info_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ttk.Frame(master)

        label = ttk.Label(frame, text='Financial year start:')
        label.grid(row=0, column=0, sticky=tk.E)
        label = ttk.Label(frame, textvariable=self.year_start)
        label.grid(row=0, column=1, sticky=tk.W)

        label = ttk.Label(frame, text='Payments for (months):')
        label.grid(row=1, column=0, sticky=tk.E)
        label = ttk.Label(frame, textvariable=self.payment_months)
        label.grid(row=1, column=1, sticky=tk.W)

        label = ttk.Label(frame, text='Rebate per F2F session:')
        label.grid(row=2, column=0, sticky=tk.E)
        label = ttk.Label(frame, textvariable=self.rebate_f2f)
        label.grid(row=2, column=1, sticky=tk.W)

        label = ttk.Label(frame, text='Rebate per BBO session:')
        label.grid(row=3, column=0, sticky=tk.E)
        label = ttk.Label(frame, textvariable=self.rebate_bbo)
        label.grid(row=3, column=1, sticky=tk.W)

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

    def _files_frame(self, container: tk.Frame) -> tk.Frame:
        frame = ttk.Frame(container)

        # frame.rowconfigure(tuple(range(6)), weight=1)
        frame.columnconfigure(1, weight=1)

        row = 0
        separator = separator_frame(frame, 'Inputs')
        separator.grid(row=row, column=0, columnspan=2, sticky=tk.EW)

        row += 1
        label = ttk.Label(frame, text='Input directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.input_dir, width=75,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='Member\'s database')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.membership_file, width=25,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='F2F attendance file')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.f2f_input_file, width=25,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='BBO attendance file')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.bbo_input_file, width=25,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='Brought forward file')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.cf_input_file, width=25,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        separator = separator_frame(frame, 'Output files')
        separator.grid(row=row, column=0, columnspan=2, sticky=tk.EW)

        row += 1
        label = ttk.Label(frame, text='output directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.output_dir, width=75,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='F2F attendance report')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.f2f_att_report, width=25,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='F2F payment file')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.f2f_rebate_file, width=25,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='BBO Attendance_report')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.bbo_att_report, width=25,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='BBO payment file')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.bbo_rebate_file, width=25,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='Carried forward file')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.cf_output_file, width=25,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button('build', self._create_rebate_files),
            frame.icon_button('exit', self._dismiss)
        ]
        return frame

    def _create_rebate_files(self, *args) -> None:
        """Call the calculation process."""
        # pylint: disable=no-member
        if not check_files(self, self.rebate_files()):
            return
        if not check_dirs(self):
            return

        input_dir = self.config.input_dir
        context = Context(
            # Dates
            self.session.period_start,
            self.session.period_end,

            # Files
            Path(input_dir, self.membership_file.get()),

            # text.F2F
            Path(input_dir, self.f2f_input_file.get()),
            Path(self.session.period_output_dir, self.session.f2f_report_file),
            Path(self.session.period_output_dir, self.session.f2f_rebate_file),

            # text. BBO
            Path(input_dir, self.bbo_input_file.get()),
            Path(self.session.period_output_dir, self.session.bbo_report_file),
            Path(self.session.period_output_dir, self.session.bbo_rebate_file),

            # C/F
            Path(input_dir, self.cf_input_file.get()),
            Path(self.session.period_output_dir, self.cf_output_file.get()),
        )

        rebate_report = RebateProcess(context)
        result = rebate_report.create_files()
        if result == rebate_report.OK:
            self._rebate_success(rebate_report)
        elif result and isinstance(result, str):
            messagebox.showerror(
                title='Process error',
                message=result,
                parent=self.root,
            )
        self.root.destroy()

    def _rebate_success(self, report: RebateProcess):
        dlg = ReportFrame(self, report)
        self.root.wait_window(dlg.root)

    def rebate_files(self) -> tuple[Path]:
        # pylint: disable=no-member
        return (
            Path(self.config.input_dir, self.membership_file.get()),
            Path(self.config.input_dir, self.f2f_input_file.get()),
            Path(self.config.input_dir, self.bbo_input_file.get()),
            Path(self.config.input_dir, self.cf_input_file.get()),
        )

    def _got_focus(self, *args) -> None:
        # pylint: disable=no-member
        self.config = get_config()
        self.payment_months.set(self.config.payment_months)
        self.rebate_f2f.set(f'{self.config.rebate_f2f / 100:.2f} (£)')
        self.rebate_bbo.set(f'{self.config.rebate_bbo / 100:.2f} ($)')

        self.session = Session()
        month = datetime(2000, self.session.year_start, 1).strftime('%b')
        self.year_start.set(f'{self.session.year_start} ({month})')
        self.date_message.set(self.session.date_message)
        self.input_dir.set(self.config.input_dir)
        self.output_dir.set(self.config.output_dir)
        self.membership_file.set(self.session.membership_file)
        self.f2f_input_file.set(self.session.f2f_input_file)
        self.f2f_att_report.set(self.session.f2f_report_file)
        self.f2f_rebate_file.set(self.session.f2f_rebate_file)
        self.bbo_input_file.set(self.session.bbo_input_file)
        self.bbo_att_report.set(self.session.bbo_report_file)
        self.bbo_rebate_file.set(self.session.bbo_rebate_file)
        self.cf_input_file.set(self.session.cf_input_file)
        self.cf_output_file.set(self.session.cf_output_file)

    def _dismiss(self, *args):
        self.root.destroy()
