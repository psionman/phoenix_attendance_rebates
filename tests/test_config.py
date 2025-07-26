from pathlib import Path

from attendance_rebates.config import get_config, save_config


def test_config_no_directory(mocker):
    mocker.patch(
        'attendance_rebates.config.CONFIG_PATH',
        Path(
            Path(__file__).parent,
            'test_data',
            'not a directory',
            'config.toml')
        )

    config = get_config()
    assert config.year_start == 5


def test_config_save(mocker):
    mocker.patch(
        'attendance_rebates.config.CONFIG_PATH',
        Path(
            Path(__file__).parent,
            'test_data',
            'config',
            'config.toml')
        )

    config = get_config()
    if config.path.is_file():
        config.path.unlink()

    config = get_config()
    config.update('year_start', 6)
    saved_config = save_config(config)
    assert save_config
    assert saved_config.year_start == 6

    read_config = get_config()
    assert read_config.year_start == 6
