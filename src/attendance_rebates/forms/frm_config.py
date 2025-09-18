import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from psiutils.widgets import separator_frame, clickable_widget
from psiutils. buttons import ButtonFrame, IconButton
from psiutils.utilities import window_resize, geometry
from psiutils.constants import PAD

from attendance_rebates.constants import (
    APP_TITLE, REBATE_MAXIMUM, REBATE_INCREMENT, ALLOWED_PAYMENT_MONTHS,
    CLUB_MIN, CLUB_MAX)
from attendance_rebates.config import get_config
import attendance_rebates.text as txt
from attendance_rebates import logger


FIELDS = {
    "year_start": tk.IntVar,
    "email_flag_club": tk.IntVar,
    "rebate_club": tk.IntVar,
    "sessions_club": tk.IntVar,
    "carried_forward_club": tk.IntVar,
    "quarter_club": tk.IntVar,
    "brought_forward_club": tk.IntVar,
    "payment_months": tk.IntVar,
    "rebate_f2f": tk.IntVar,
    "rebate_bbo": tk.IntVar,
    "download_folder": tk.StringVar,
    "output_dir": tk.StringVar,
}


class ConfigFrame():
    year_start: tk.IntVar
    email_flag_club: tk.IntVar
    rebate_club: tk.IntVar
    sessions_club: tk.IntVar
    carried_forward_club: tk.IntVar
    quarter_club: tk.IntVar
    brought_forward_club: tk.IntVar
    payment_months: tk.IntVar
    rebate_f2f: tk.IntVar
    rebate_bbo: tk.IntVar
    download_folder: tk.StringVar
    output_dir: tk.StringVar

    def __init__(self, parent):
        self.root = tk.Toplevel(parent.root)
        self.parent = parent
        self.session = parent.session
        self.config = get_config()
        config = self.config

        for field, f_type in FIELDS.items():
            if f_type is tk.StringVar:
                setattr(self, field, self._stringvar(getattr(config, field)))
            elif f_type is tk.IntVar:
                setattr(self, field, self._intvar(getattr(config, field)))
            elif f_type is tk.BooleanVar:
                setattr(self, field, self._boolvar(getattr(config, field)))

        self.button_frame = None

        self._show()

    def _stringvar(self, value: str) -> tk.StringVar:
        stringvar = tk.StringVar(value=value)
        stringvar.trace_add('write', self._check_value_changed)
        return stringvar

    def _intvar(self, value: int) -> tk.IntVar:
        intvar = tk.IntVar(value=value)
        intvar.trace_add('write', self._check_value_changed)
        return intvar

    def _boolvar(self, value: bool) -> tk.BooleanVar:
        boolvar = tk.BooleanVar(value=value)
        boolvar.trace_add('write', self._check_value_changed)
        return boolvar

    def _show(self) -> None:
        root = self.root
        root.geometry(geometry(self.config, __file__))
        root.transient(self.parent.root)
        root.title(f'{APP_TITLE} - {txt.CONFIG}')

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

        self.button_frame = self._button_frame(frame)
        self.button_frame.grid(row=4, column=0, sticky=tk.EW, padx=PAD, pady=PAD)
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
            frame, txt.OPEN, 'open', self._get_download_folder)
        button.grid(row=row, column=3, sticky=tk.W, padx=PAD)

        row += 1
        label = ttk.Label(frame, text='Output directory')
        label.grid(row=row, column=0, sticky=tk.E, padx=PAD)
        entry = ttk.Entry(frame,  textvariable=self.output_dir)
        entry.grid(row=row, column=1, columnspan=2, sticky=tk.EW)
        button = IconButton(
            frame, txt.OPEN, 'open', self._get_output_dir)
        button.grid(row=row, column=3, sticky=tk.W, padx=PAD, pady=PAD)
        clickable_widget(button)

        return frame

    def _button_frame(self, master: tk.Frame) -> tk.Frame:
        frame = ButtonFrame(master, tk.HORIZONTAL)
        frame.buttons = [
            frame.icon_button('save', self._save_config, True),
            frame.icon_button('exit', self._dismiss)
        ]
        frame.disable()
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
        download_dir = filedialog.askdirectory(
            title='Downloads folder',
            initialdir=self.config.input_dir,
            parent=self.root,
            )
        if download_dir:
            self.download_folder.set(download_dir)
            self.config.input_dir = download_dir

    def _get_output_dir(self):
        """Set output directory."""
        output_dir = filedialog.askdirectory(
            title='Output directory',
            initialdir=self.config.output_dir,
            parent=self.root,
            )
        if output_dir:
            self.output_dir.set(output_dir)
            self.config.output_dir = output_dir

    def _check_value_changed(self, *args) -> None:
        enable = bool(self._config_changes())
        self.button_frame.enable(enable)

    def save_config(self, *args) -> int:
        """Save the config."""
        changes = {field: f'(old value={change[0]}, new_value={change[1]})'
                   for field, change in self._config_changes().items()}
        logger.info(
            "Config saved",
            changes=changes
        )

        for field in FIELDS:
            self.config.config[field] = getattr(self, field).get()
        return self.config.save()

    def _config_changes(self) -> dict:
        stored = self.config.config
        return {
            field: (stored[field], getattr(self, field).get())
            for field in FIELDS
            if stored[field] != getattr(self, field).get()
        }

    def _dismiss(self, *args):
        self.root.destroy()
