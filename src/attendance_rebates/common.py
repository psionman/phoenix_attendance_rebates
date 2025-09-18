from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from psiutils.constants import CSV_FILE_TYPES
from attendance_rebates import logger


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
    return all(_file_exists(frame, path) for path in path_list)


def _file_exists(parent, path):
    """Check file exists, if not, display a notification."""
    if path.is_file():
        return True
    logger.warning(
        'file does not exist',
        path=str(path),
    )
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
