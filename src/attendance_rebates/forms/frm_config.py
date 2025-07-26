import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from psiutils.widgets import separator_frame, clickable_widget
from psiutils. buttons import ButtonFrame, IconButton
from psiutils.utilities import window_resize, geometry
from psiutils.constants import PAD

from constants import (APP_TITLE, REBATE_MAXIMUM, REBATE_INCREMENT,
                       ALLOWED_PAYMENT_MONTHS, CLUB_MIN, CLUB_MAX)
from config import get_config
import text


class ConfigFrame():
    def __init__(self, parent):
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.session = parent.session
        self.config = get_config()
        config = self.config

        # tk variables
        self.year_start = tk.IntVar(value=config.year_start)
        self.email_flag_club = tk.IntVar(value=config.email_flag_club)
        self.rebate_club = tk.IntVar(value=config.rebate_club)
        self.sessions_club = tk.IntVar(value=config.sessions_club)
        self.carried_forward_club = tk.IntVar(
            value=config.carried_forward_club)
        self.quarter_club = tk.IntVar(value=config.quarter_club)
        self.brought_forward_club = tk.IntVar(
            value=config.brought_forward_club)
        self.payment_months = tk.IntVar(value=config.payment_months)
        self.rebate_f2f = tk.IntVar(value=config.rebate_f2f)
        self.rebate_bbo = tk.IntVar(value=config.rebate_bbo)
        self.download_folder = tk.StringVar(value=config.input_dir)
        self.output_dir = tk.StringVar(value=config.output_dir)

        self.show()

    def show(self) -> None:
        root = self.root
        root.geometry(geometry(self.config, __file__))
        root.transient(self.parent.root)
        root.title(f'{APP_TITLE} - {text.CONFIG}')

        root.bind('<Control-x>', self._dismiss)
        root.bind('<Control-s>', self._save_config)
        root.bind('<Configure>',
                  lambda event, arg=None: window_resize(self, __file__))

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        main_frame = self._main_frame(root)
        main_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=PAD, pady=PAD)

        sizegrip = ttk.Sizegrip(self.root)
        sizegrip.grid(sticky=tk.SE)

    def _main_frame(self, master: tk.Frame) -> ttk.Frame:
        frame = ttk.Frame(master)
        frame.grid(row=0, column=0, sticky=tk.NSEW)

        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)

        frame.columnconfigure(0, weight=1)  # Essential
        config_frame = self._config_frame(frame)
        config_frame.grid(row=1, column=0, sticky=tk.NSEW, padx=PAD)

        button_frame = self._button_frame(frame)
        button_frame.grid(row=4, column=0, sticky=tk.EW, padx=PAD, pady=PAD)
        return frame

    def _config_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ttk.Frame(master)
        frame.columnconfigure(2, weight=1)

        row = 0
        separator = separator_frame(frame, 'System settings')
        separator.grid(row=row, column=0, columnspan=4, sticky=tk.EW)

        row += 1
        label = ttk.Label(frame, text='Financial year start')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)

        spinbox = ttk.Spinbox(
            frame,
            width=2,
            from_=1,
            to=12,
            increment=1,
            textvariable=self.year_start,
            # command=self.session.calculate_dates
        )
        spinbox.grid(row=row, column=1, sticky=tk.EW)
        clickable_widget(spinbox)

        row += 1
        label = ttk.Label(frame, text='Payments for (months)')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)

        combobox = ttk.Combobox(
            frame,
            width=5,
            values=ALLOWED_PAYMENT_MONTHS,
            textvariable=self.payment_months,
            )
        combobox.grid(row=row, column=1, sticky=tk.EW)
        # combobox.bind(
        #     '<<ComboboxSelected>>',
        #     self._change_cmb_period_months
        #     )
        clickable_widget(combobox)

        row += 1
        label = ttk.Label(frame, text='Rebate per F2F session (pence)')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)
        spinbox = ttk.Spinbox(
            frame,
            width=4,
            from_=0,
            to=REBATE_MAXIMUM,
            increment=REBATE_INCREMENT,
            textvariable=self.rebate_f2f,
            )
        spinbox.grid(row=row, column=1, sticky=tk.EW)
        clickable_widget(spinbox)

        row += 1
        label = ttk.Label(frame, text='Rebate per BBO session (cents)')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)
        spinbox = ttk.Spinbox(
            frame,
            width=4,
            from_=0,
            to=REBATE_MAXIMUM,
            increment=REBATE_INCREMENT,
            textvariable=self.rebate_bbo,
            )
        spinbox.grid(row=row, column=1, sticky=tk.EW)
        clickable_widget(spinbox)

        row += 1
        separator = separator_frame(frame, 'Club Field Numbers')
        separator.grid(row=row, column=0, columnspan=4, sticky=tk.EW)

        row += 1
        label = ttk.Label(frame, text='Email flag: CLUB')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)
        spinbox = self._create_spin_box(frame, self.email_flag_club)
        spinbox.grid(row=row, column=1, sticky=tk.EW)
        clickable_widget(spinbox)

        row += 1
        label = ttk.Label(frame, text='Brought forward: CLUB')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)
        spinbox = self._create_spin_box(
            frame,
            self.brought_forward_club)
        spinbox.grid(row=row, column=1, sticky=tk.EW)
        clickable_widget(spinbox)

        row += 1
        label = ttk.Label(frame, text='Rebate amount: CLUB')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)
        spinbox = self._create_spin_box(frame, self.rebate_club)
        spinbox.grid(row=row, column=1, sticky=tk.EW)
        clickable_widget(spinbox)

        row += 1
        label = ttk.Label(frame, text='Sessions: CLUB')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)
        spinbox = self._create_spin_box(frame, self.sessions_club)
        spinbox.grid(row=row, column=1, sticky=tk.EW)
        clickable_widget(spinbox)

        row += 1
        label = ttk.Label(frame, text='Carried forward: CLUB')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)
        spinbox = self._create_spin_box(
            frame,
            self.carried_forward_club
            )
        spinbox.grid(row=row, column=1, sticky=tk.EW)
        clickable_widget(spinbox)

        row += 1
        label = ttk.Label(frame, text='Quarter start: CLUB')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)
        spinbox = self._create_spin_box(frame, self.quarter_club)
        spinbox.grid(row=row, column=1, sticky=tk.EW)
        clickable_widget(spinbox)

        row += 1
        separator = separator_frame(frame, 'Directories')
        separator.grid(row=row, column=0, columnspan=4, sticky=tk.EW)

        row += 1
        label = ttk.Label(frame, text='Input directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)
        entry = ttk.Entry(frame,  textvariable=self.download_folder)
        entry.grid(row=row, column=1, columnspan=2, sticky=tk.EW)
        button = IconButton(
            frame, text.OPEN, 'open', self._get_download_folder)
        button.grid(row=row, column=3, sticky=tk.W, padx=PAD)

        row += 1
        label = ttk.Label(frame, text='Output directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)
        entry = ttk.Entry(frame,  textvariable=self.output_dir)
        entry.grid(row=row, column=1, columnspan=2, sticky=tk.EW)
        button = IconButton(
            frame, text.OPEN, 'open', self._get_output_dir)
        button.grid(row=row, column=3, sticky=tk.W, padx=PAD, pady=PAD)
        clickable_widget(button)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button('save', True, self._save_config),
            frame.icon_button('exit', False, self._dismiss)
        ]
        return frame

    def _save_config(self):
        self.save_config(self)
        self._dismiss()

    def _create_spin_box(self, frame, textvariable):
        return ttk.Spinbox(
            frame,
            width=5,
            from_=CLUB_MIN,
            to=CLUB_MAX,
            increment=1,
            textvariable=textvariable,
        )

    def _get_download_folder(self):
        """Set Downloads directory."""
        dir = filedialog.askdirectory(
            title='Downloads folder',
            initialdir=self.config.input_dir,
            parent=self.root,
            )
        if dir:
            self.download_folder.set(dir)
            self.config.input_dir = dir
            self.get_file_paths()

    def _get_output_dir(self):
        """Set output directory."""
        dir = filedialog.askdirectory(
            title='Output directory',
            initialdir=self.config.output_dir,
            parent=self.root,
            )
        if dir:
            self.output_dir.set(dir)
            self.config.output_dir = dir
            self.get_file_paths()

    # def _change_cmb_period_months(self, *args) -> None:
    #     """Relay function on change of combobox."""
    #     self.calculate_dates()

    def save_config(self, *args) -> int:
        # Email attributes
        config = self.config.config
        config['email_flag_club'] = self.email_flag_club.get()
        config['brought_forward_club'] = self.brought_forward_club.get()
        config['rebate_club'] = self.rebate_club.get()
        config['carried_forward_club'] = self.carried_forward_club.get()
        config['sessions_club'] = self.sessions_club.get()

        # Dates
        config['year_start'] = self.year_start.get()

        # Rebates
        config['payment_months'] = self.payment_months.get()
        config['rebate_f2f'] = self.rebate_f2f.get()
        config['rebate_bbo'] = self.rebate_bbo.get()

        # Folders
        config['download_folder'] = self.download_folder.get()
        config['output_dir'] = self.output_dir.get()

        result = self.config.save()
        return result

    def _dismiss(self, *args):
        self.root.destroy()
