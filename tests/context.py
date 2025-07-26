import datetime
from pathlib import Path

from attendance_rebates.rebate_process import Context as RebateContext
from attendance_rebates.email_process import Context as EmailContext


test_data_dir = Path(Path(__file__).parent, 'test_data')

rebate_context = RebateContext(
    # Dates
    datetime.datetime(2023, 8, 1, 0, 0),
    datetime.datetime(2023, 10, 1, 0, 0),

    # Files
    Path(test_data_dir, 'inputs', 'membership_202311.csv'),

    # F2F
    Path(test_data_dir, 'inputs', 'f2f_2023_11.csv'),
    Path(test_data_dir, 'outputs', 'f2f_att_report_2023_11.csv'),
    Path(test_data_dir, 'outputs', 'f2f_att_rebate_2023_11.csv'),

    # BBO
    Path(test_data_dir, 'inputs', 'bbo_2023_11.csv'),
    Path(test_data_dir, 'outputs', 'bbo_att_report_2023_11.csv'),
    Path(test_data_dir, 'outputs', 'bbo_att_rebate_2023_11.csv'),

    # C/F
    Path(test_data_dir, 'inputs', 'cf_2023_08.csv'),
    Path(test_data_dir, 'outputs', 'cf_2023_11.csv'),
)


f2f_email_context = EmailContext(
    'Aug 2023',
    Path(test_data_dir, 'inputs', 'membership_202311.csv'),
    Path(test_data_dir, 'outputs', 'f2f_att_report_2023_11.csv'),
    Path(test_data_dir, 'outputs', 'f2f_email_2023_11.csv'),
    None
)


bbo_email_context = EmailContext(
    'Aug 2023',
    Path(test_data_dir, 'inputs', 'membership_202311.csv'),
    Path(test_data_dir, 'outputs', 'bbo_att_report_2023_11.csv'),
    Path(test_data_dir, 'outputs', 'bbo_email_2023_11.csv'),
    None
)
