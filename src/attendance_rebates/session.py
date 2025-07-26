"""Session-wide variables and settings."""


from pathlib import Path
from datetime import datetime
from dateutil import relativedelta


from attendance_rebates.config import get_config
from attendance_rebates.constants import DDMMYYYY, YYYYMM
import attendance_rebates.text as text

date_delta = relativedelta.relativedelta


class Session():
    def __init__(self, config: dict = None) -> None:
        self.config = config
        if not config:
            self.config = get_config()

        self.year_start = self.config.year_start
        self.period_months = self.config.payment_months

        period_starts = self._get_period_starts(self.year_start)
        self.period_date = period_starts[-2].strftime(DDMMYYYY)
        self.base_date = period_starts[-1]

        self.period_start = (self.base_date - date_delta(
            months=self.config.payment_months))
        self.period_end = (self.base_date - date_delta(days=1))
        self.date_message = (
            f'Rebates for period {self.period_start.strftime(DDMMYYYY)} to '
            f'{self.period_end.strftime(DDMMYYYY)}'
            )

        short_date = self.base_date.strftime('%Y%m')
        self.period_output_dir = Path(self.config.output_dir, short_date)
        self.get_file_paths()

    def _get_period_starts(self, year_start: int,) -> list[datetime]:
        """
        Return a list of period start dates from a year ago
        to the latest before today.
        """
        period_starts = []
        today = datetime.now()
        period_date = datetime(today.year - 1, year_start, 1)
        while period_date <= today:
            period_starts.append(period_date)
            period_date = period_date + date_delta(months=self.period_months)
        return period_starts

    def get_file_paths(self) -> None:
        """Populate file name variables."""
        CF_PREFIX = text.CF_PREFIX
        CSV = text.CSV
        EMAIL = text.EMAIL
        BBO = text.BBO
        F2F = text.F2F

        year_month = self.base_date.strftime(YYYYMM)

        self.membership_file = f'{text.MEMBERSHIP}_{year_month}.{CSV}'

        # Input file names
        self.f2f_input_file = f'{F2F}_{year_month}.{CSV}'
        # e.g. f2f_202502.csv

        self.bbo_input_file = f'{BBO}_{year_month}.{CSV}'
        # e.g. bbo_202502.csv

        self.cf_input_file = f'{CF_PREFIX}_{self._previous_date_text()}.{CSV}'
        # e.g. cf_202411.csv

        # Report file names
        report_file_name = f'{text.REBATE_REPORT}_{year_month}.{CSV}'
        self.f2f_report_file = f'{F2F}_{report_file_name}'
        self.bbo_report_file = f'{BBO}_{report_file_name}'

        # Rebate file names
        rebate_file_name = f'{text.REBATE_FILE_PREFIX}_{year_month}.{CSV}'
        self.f2f_rebate_file = f'{F2F}_{rebate_file_name}'
        self.bbo_rebate_file = f'{BBO}_{rebate_file_name}'

        # cf output file
        self.cf_output_file = f'{CF_PREFIX}_{year_month}.{CSV}'

        #  Email input files
        self.f2f_email_input_file = f'{F2F}_{report_file_name}'
        self.bbo_email_input_file = f'{BBO}_{report_file_name}'

        # Email output files
        self.f2f_email_output_file = f'{F2F}_{EMAIL}_{year_month}.{CSV}'
        self.bbo_email_output_file = f'{BBO}_{EMAIL}_{year_month}.{CSV}'

    def _previous_date_text(self) -> str:
        add_date = date_delta(months=self.config.payment_months)
        previous_date = self.base_date - add_date
        return previous_date.strftime(YYYYMM).lower()
