from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from psiutils.constants import CSV_FILE_TYPES, PAD


def header_frame(container, text, row):
    frame = ttk.Frame(container)
    frame.grid(row=row, column=0)
    header = ttk.Label(frame, text=text, font=('Arial', 16))
    header.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=PAD)


def get_csv_file(frame, title, initialdir, initialfile):
    """Set path to members database file."""
    filename = filedialog.askopenfilename(
        title=title,
        initialdir=initialdir,
        initialfile=initialfile,
        filetypes=CSV_FILE_TYPES,
        parent=frame,
        )
    if filename:
        initialfile.set(Path(filename).name)


def check_files(frame, path_list):
    """Ensure that all files exist."""
    for path in path_list:
        if not _file_exists(frame, path):
            return False
    return True


def _file_exists(parent, path):
    """Check file exists, if not, display a notification."""
    if path.is_file():
        return True
    msg = f'File does not exist: \n{path}'
    messagebox.showerror(title='File error', message=msg, parent=parent.root)
    return False


def check_dirs(parent: tk.Frame):
    """Ensure that all files exist."""
    path_list = [
        Path(parent.session.period_output_dir),
    ]
    for path in path_list:
        path.mkdir(parents=True, exist_ok=True)
    return True
