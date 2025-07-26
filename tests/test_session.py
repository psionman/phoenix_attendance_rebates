
from datetime import datetime
from freezegun import freeze_time
from pathlib import Path

from attendance_rebates.session import Session
from attendance_rebates.config import get_config


# freeze_time sets the value of datetime.now()
@freeze_time('2023-11-14')
def test_base_date():
    session = Session()
    assert session.base_date == datetime(2023, 11, 1)


@freeze_time('2023-11-14')
def test_file_names():
    input_dir = Path(Path(__file__).parent.parent, 'test_data', 'inputs')
    output_dir = Path(Path(__file__).parent.parent, 'test_data', 'outputs')
    config = get_config()
    config.update('input_dir', input_dir)
    config.update('output_dir',  output_dir)

    session = Session(config)
    assert session.period_output_dir == Path(output_dir, '202311')
    assert session.membership_file == 'membership_202311.csv'
    assert session.f2f_input_file == 'f2f_202311.csv'
    assert session.bbo_input_file == 'bbo_202311.csv'
    assert session.cf_input_file == 'cf_202308.csv'
    assert session.cf_output_file == 'cf_202311.csv'
    assert session.f2f_report_file == 'f2f_att_report_202311.csv'
    assert session.bbo_report_file == 'bbo_att_report_202311.csv'
    assert session.f2f_rebate_file == 'f2f_att_rebate_202311.csv'
    assert session.bbo_rebate_file == 'bbo_att_rebate_202311.csv'


@freeze_time('2024-1-14')
def test_dates_jun_jan():
    config = get_config()
    assert _check_base_date(config, 6, 6, datetime(2023, 12, 1))
    assert _check_base_date(config, 6, 4, datetime(2023, 10, 1))
    assert _check_base_date(config, 6, 3, datetime(2023, 12, 1))
    assert _check_base_date(config, 6, 2, datetime(2023, 12, 1))

    assert _check_period_start(config, 6, 6, datetime(2023, 6, 1))
    assert _check_period_start(config, 6, 4, datetime(2023, 6, 1))
    assert _check_period_start(config, 6, 3, datetime(2023, 9, 1))
    assert _check_period_start(config, 6, 2, datetime(2023, 10, 1))

    assert _check_period_end(config, 6, 6, datetime(2023, 11, 30))
    assert _check_period_end(config, 6, 4, datetime(2023, 9, 30))
    assert _check_period_end(config, 6, 3, datetime(2023, 11, 30))
    assert _check_period_end(config, 6, 2, datetime(2023, 11, 30))

    assert _check_period_output_dir(config, 6, 6, '202312')
    assert _check_period_output_dir(config, 6, 4, '202310')
    assert _check_period_output_dir(config, 6, 3, '202312')
    assert _check_period_output_dir(config, 6, 2, '202312')


@freeze_time('2024-1-14')
def test_dates_may_jan():
    config = get_config()
    assert _check_base_date(config, 5, 6, datetime(2023, 11, 1))
    assert _check_base_date(config, 5, 4, datetime(2024, 1, 1))
    assert _check_base_date(config, 5, 3, datetime(2023, 11, 1))
    assert _check_base_date(config, 5, 2, datetime(2024, 1, 1))

    assert _check_period_start(config, 5, 6, datetime(2023, 5, 1))
    assert _check_period_start(config, 5, 4, datetime(2023, 9, 1))
    assert _check_period_start(config, 5, 3, datetime(2023, 8, 1))
    assert _check_period_start(config, 5, 2, datetime(2023, 11, 1))

    assert _check_period_end(config, 5, 6, datetime(2023, 10, 31))
    assert _check_period_end(config, 5, 4, datetime(2023, 12, 31))
    assert _check_period_end(config, 5, 3, datetime(2023, 10, 31))
    assert _check_period_end(config, 5, 2, datetime(2023, 12, 31))

    assert _check_period_output_dir(config, 5, 6, '202311')
    assert _check_period_output_dir(config, 5, 4, '202401')
    assert _check_period_output_dir(config, 5, 3, '202311')
    assert _check_period_output_dir(config, 5, 2, '202401')


@freeze_time('2023-11-14')
def test_dates_may_nov():
    config = get_config()
    assert _check_base_date(config, 5, 6, datetime(2023, 11, 1))
    assert _check_base_date(config, 5, 4, datetime(2023, 9, 1))
    assert _check_base_date(config, 5, 3, datetime(2023, 11, 1))
    assert _check_base_date(config, 5, 2, datetime(2023, 11, 1))

    assert _check_period_start(config, 5, 6, datetime(2023, 5, 1))
    assert _check_period_start(config, 5, 4, datetime(2023, 5, 1))
    assert _check_period_start(config, 5, 3, datetime(2023, 8, 1))
    assert _check_period_start(config, 5, 2, datetime(2023, 9, 1))

    assert _check_period_end(config, 5, 6, datetime(2023, 10, 31))
    assert _check_period_end(config, 5, 4, datetime(2023, 8, 31))
    assert _check_period_end(config, 5, 3, datetime(2023, 10, 31))
    assert _check_period_end(config, 5, 2, datetime(2023, 10, 31))

    assert _check_period_output_dir(config, 5, 6, '202311')
    assert _check_period_output_dir(config, 5, 4, '202309')
    assert _check_period_output_dir(config, 5, 3, '202311')
    assert _check_period_output_dir(config, 5, 2, '202311')



@freeze_time('2023-10-14')
def test_dates_may_oct():
    config = get_config()
    assert _check_base_date(config, 5, 6, datetime(2023, 5, 1))
    assert _check_base_date(config, 5, 4, datetime(2023, 9, 1))
    assert _check_base_date(config, 5, 3, datetime(2023, 8, 1))
    assert _check_base_date(config, 5, 2, datetime(2023, 9, 1))

    assert _check_period_start(config, 5, 6, datetime(2022, 11, 1))
    assert _check_period_start(config, 5, 4, datetime(2023, 5, 1))
    assert _check_period_start(config, 5, 3, datetime(2023, 5, 1))
    assert _check_period_start(config, 5, 2, datetime(2023, 7, 1))

    assert _check_period_end(config, 5, 6, datetime(2023, 4, 30))
    assert _check_period_end(config, 5, 4, datetime(2023, 8, 31))
    assert _check_period_end(config, 5, 3, datetime(2023, 7, 31))
    assert _check_period_end(config, 5, 2, datetime(2023, 8, 31))

    assert _check_period_output_dir(config, 5, 6, '202305')
    assert _check_period_output_dir(config, 5, 4, '202309')
    assert _check_period_output_dir(config, 5, 3, '202308')
    assert _check_period_output_dir(config, 5, 2, '202309')


def _check_base_date(
        config,
        year_start: int,
        payment_months: int,
        check_date: datetime
        ):
    """Check dates based on year start and payment months."""
    config.update('year_start', year_start)
    config.update('payment_months', payment_months)
    session = Session(config)
    return session.base_date == check_date


def _check_period_start(
        config,
        year_start: int,
        payment_months: int,
        check_date: datetime
        ):

    config.update('year_start', year_start)
    config.update('payment_months', payment_months)
    session = Session(config)
    return session.period_start == check_date


def _check_period_end(
        config,
        year_start: int,
        payment_months: int,
        check_date: datetime
        ):

    config.update('year_start', year_start)
    config.update('payment_months', payment_months)
    session = Session(config)

    return session.period_end == check_date


def _check_period_output_dir(
        config,
        year_start: int,
        payment_months: int,
        check_date: str
        ):

    config.update('year_start', year_start)
    config.update('payment_months', payment_months)
    session = Session(config)
    return check_date == session.period_output_dir.parts[-1]
