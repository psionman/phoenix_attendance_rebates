""" Constants to support the application."""
from pathlib import Path
from appdirs import user_config_dir, user_data_dir



# Config
APP_NAME = 'phoenix_player_rebates'
APP_AUTHOR = 'phoenix'
APP_TITLE = 'Players\'  attendance rebates'

CONFIG_PATH = Path(user_config_dir(APP_NAME, APP_AUTHOR), 'config.toml')
USER_DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
CONFIG_TEXT = 'Preferences'
ICON_FILE = Path(Path(__file__).parent, 'images/icon.png')

# Colours
INFO_COLOUR = 'green'
WARNING_COLOUR = 'red'

# Date formats
YYYYMMDD = '%Y%m%d'
DDMMYYYY = '%d %b %Y'
MM_SPACE_YYYY = '%b %Y'
YYYYMM = '%Y%m'

# Files and directories

NO_FILE_SELECTED = 'No file selected'
EBU_KEY = 'EBU'
BBO_KEY = 'BBO username'

CSV_FILE_TYPES = (
    ('csv files', '*.csv'),
    ('All files', '*.*')
)

# Report
SHOW_ALL_RECORDS = False
REPORT_FIELDS = [
    'EBU',
    'First name',
    'Surname',
    'Email',
    'Attendance b/f',
    'Attendance',
    'Qualifying attendance',
    'Attendance c/f',
    'rebate',
]


CLUB_MIN = 5
CLUB_MAX = 10
HAND = 'hand2'

ALLOWED_PAYMENT_MONTHS = [1, 2, 3, 4, 6, 12]
REBATE_MAXIMUM = 100000
REBATE_INCREMENT = 25

FORMATS = ['bbo', 'f2f']

REBATE_MAXIMUM = 100000
REBATE_INCREMENT = 25


SEPARATOR = '-'
PATH_WIDTH = 75
TEXT_WIDTH = 20

AUTHOR = 'Jeff Watkins'
