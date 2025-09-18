from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from psiutils.widgets import separator_frame
from psiutils. buttons import ButtonFrame
from psiutils.utilities import window_resize, geometry
from psiutils.constants import PAD

from attendance_rebates.config import get_config
from attendance_rebates.session import Session
from attendance_rebates.common import check_files, check_dirs
from attendance_rebates.email_process import EmailProcess, Context

from attendance_rebates.menu import MainMenu

TITLE = 'Email reports'


class EmailFrame():
    def __init__(self, parent):
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.session = Session()
        self.config = get_config()

        # tk variables
        self.year_start = tk.StringVar()
        self.date_message = tk.StringVar()
        self.payment_months = tk.StringVar()
        self.rebate_f2f = tk.StringVar()
        self.rebate_bbo = tk.StringVar()
        self.membership_file = tk.StringVar()
        self.file_message = tk.StringVar()
        self.members_text = tk.StringVar()
        self.email_file_text = tk.StringVar()
        self.f2f_att_report = tk.StringVar()
        self.bbo_att_report = tk.StringVar()
        self.f2f_email_output_file = tk.StringVar()
        self.bbo_email_output_file = tk.StringVar()

        self._show()
        self._got_focus()

    def _show(self) -> None:
        root = self.root
        root.geometry(geometry(self.config, __file__))
        root.transient(self.parent.root)
        root.title(TITLE)

        root.bind('<Control-q>', self._dismiss)
        root.bind('<Control-p>', self._create_email_files)
        self.root.bind("<FocusIn>", self._got_focus)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_menu = MainMenu(self)
        main_menu.create()

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(self.root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
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

    def _files_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ttk.Frame(master)

        frame.columnconfigure(1, weight=1)

        row = 0
        separator = separator_frame(frame, 'Input files')
        separator.grid(row=row, column=0, columnspan=2, sticky=tk.EW)

        row += 1
        label = ttk.Label(frame, text='Member\'s database')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.membership_file, width=25,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='F2F attendance report')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.f2f_att_report, width=25,
                          relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='BBO attendance report')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.bbo_att_report,
                          width=25, relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        separator = separator_frame(frame, 'Output files')
        separator.grid(row=row, column=0, columnspan=2, sticky=tk.EW)

        row += 1
        label = ttk.Label(frame, text='F2F email report')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.f2f_email_output_file,
                          width=25, relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        row += 1
        label = ttk.Label(frame, text='BBO email report')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD, pady=PAD)

        label = ttk.Label(frame, textvariable=self.bbo_email_output_file,
                          width=25, relief=tk.SUNKEN, anchor=tk.W)
        label.grid(row=row, column=1, sticky=tk.W)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button('build', self._create_email_files),
            frame.icon_button('exit', self._dismiss)
        ]
        return frame

    def _create_email_files(self, *args) -> None:
        # pylint: disable=no-member
        """Create Email files."""
        if not check_files(self, self._email_files()):
            return
        if not check_dirs(self):
            return

        period_dir = self.session.period_output_dir
        result = 0

        # F2F
        context = Context(
            self.session.period_date,
            Path(self.config.input_dir, self. membership_file.get()),
            Path(period_dir, self.f2f_att_report.get()),
            Path(period_dir, self.f2f_email_output_file.get()),
            None,
        )
        result += EmailProcess(context).create_files()

        # BBO
        context = Context(
            self.session.period_date,
            Path(self.config.input_dir, self. membership_file.get()),
            Path(period_dir, self.bbo_att_report.get()),
            Path(period_dir, self.bbo_email_output_file.get()),
            Path(period_dir, 'bbo_payment_file.csv'),
        )
        result += EmailProcess(context).create_files()

        if result == 2:
            self._email_success()
        else:
            self._email_failure()
        self.root.destroy()

    def _email_files(self) -> tuple[Path]:
        # pylint: disable=no-member
        return (
            Path(self.config.input_dir, self.membership_file.get()),
            Path(self.session.period_output_dir, self.f2f_att_report.get()),
            Path(self.session.period_output_dir, self.bbo_att_report.get()),
        )

    def _email_success(self):
        # pylint: disable=no-member
        message = [
            'Email files successfully created ...',
            'Files will be found in the directory:',
            f'\'{self.config.output_dir}\'',
        ]
        messagebox.showinfo(
            title='Rebate emails',
            message='\n'.join(message),
            # parent=self.root,
        )

    def _email_failure(self):
        # pylint: disable=no-member
        line_one = "Email files error. files not created."
        line_two = f"Report directory: {self.config.output_dir}"
        msg = f'{line_one}' + '\n' + f'{line_two}'
        messagebox.showerror(title=self.title, message=msg, parent=self)

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
        self.membership_file.set(self.session.membership_file)
        self.f2f_att_report.set(self.session.f2f_email_input_file)
        self.bbo_att_report.set(self.session.bbo_email_input_file)
        self.f2f_email_output_file.set(self.session.f2f_email_output_file)
        self.bbo_email_output_file.set(self.session.bbo_email_output_file)

    def _dismiss(self, *args):
        self.root.destroy()
