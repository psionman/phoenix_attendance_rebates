from pathlib import Path
from appdirs import user_data_dir

from psiconfig import TomlConfig
from psiutils.known_paths import get_downloads_dir

from attendance_rebates.constants import CONFIG_PATH, APP_AUTHOR, APP_NAME


DEFAULT_CONFIG = {
    'email_flag_club': 5,
    'rebate_club': 6,
    'brought_forward_club': 7,
    'sessions_club': 8,
    'carried_forward_club': 9,
    'quarter_club': 10,
    'input_dir': get_downloads_dir(),  # in utilities
    'output_dir': str(Path(user_data_dir(APP_NAME, APP_AUTHOR))),
    'year_start': 5,
    'rebate_bbo': 300,
    'rebate_f2f': 250,
    'qualifying_attendances': 10,
    'payment_months': 3,
    'geometry': {},
}


def get_config() -> TomlConfig:
    """Return the config file."""
    return TomlConfig(path=CONFIG_PATH, defaults=DEFAULT_CONFIG)


def save_config(config: TomlConfig) -> TomlConfig | None:
    config.save()
    config = TomlConfig(CONFIG_PATH)
    return config


# config = get_config()
