"""
Tests for the creation of the f2f and bbo email files and the reset files.
"""

from pathlib import Path

from attendance_rebates.email_process import EmailProcess

from context import (f2f_email_context, bbo_email_context,
                     test_data_dir as data_dir)


def test_f2f_email():
    output_file = str(Path(data_dir, 'outputs', 'f2f_email_2023_11.csv'))
    reset_file = str(Path(data_dir, 'outputs', 'f2f_reset_2023_11.csv'))

    process = EmailProcess(f2f_email_context)
    assert process.create_files() == process.OK

    with open(output_file, 'r') as f_output:
        emails = f_output.read().split('\n')
    assert len(emails) == 47
    with open(reset_file, 'r') as f_reset:
        resets = f_reset.read().split('\n')
    assert len(resets) == 47

    for email in emails:
        record = email.split(',')
        if len(record) > 24 and record[1] == 'Grochowska':
            assert record[18] == 'Y'
            assert record[19] == '2.50'
            assert record[20] == '1'
            assert record[21] == '17'
            assert record[22] == '8'
            assert record[23] == 'Aug 2023'

        if len(record) > 24 and record[1] == 'Irving':
            assert record[18] == 'Y'
            assert record[19] == '5.00'
            assert record[20] == '9'
            assert record[21] == '18'
            assert record[22] == '7'
            assert record[23] == 'Aug 2023'

    for reset in resets:
        record = reset.split(',')
        if len(record) > 24 and record[1] == 'Grochowska':
            assert record[18] == 'N'
            assert record[19] == ''
            assert record[20] == ''
            assert record[21] == ''
            assert record[22] == ''
            assert record[23] == ''

        if len(record) > 24 and record[1] == 'Irving':
            assert record[18] == 'N'
            assert record[19] == ''
            assert record[20] == ''
            assert record[21] == ''
            assert record[22] == ''
            assert record[23] == ''


def test_bbo_email():
    output_file = str(Path(data_dir, 'outputs', 'bbo_email_2023_11.csv'))
    reset_file = str(Path(data_dir, 'outputs', 'bbo_reset_2023_11.csv'))

    process = EmailProcess(bbo_email_context)
    assert process.create_files() == process.OK
    with open(output_file, 'r') as f_output:
        emails = f_output.read().split('\n')
    assert len(emails) == 50
    with open(reset_file, 'r') as f_reset:
        resets = f_reset.read().split('\n')
    assert len(resets) == 50

    for email in emails:
        record = email.split(',')
        if len(record) > 24 and record[1] == 'Watkins':
            assert record[18] == 'Y'
            assert record[19] == '6.00'
            assert record[20] == '9'
            assert record[21] == '18'
            assert record[22] == '7'
            assert record[23] == 'Aug 2023'

        if len(record) > 24 and record[1] == 'Kerslake':
            assert record[18] == 'Y'
            assert record[19] == '3.00'
            assert record[20] == '1'
            assert record[21] == '12'
            assert record[22] == '3'
            assert record[23] == 'Aug 2023'

    for reset in resets:
        record = reset.split(',')
        if len(record) > 24 and record[1] == 'Watkins':
            assert record[18] == 'N'
            assert record[19] == ''
            assert record[20] == ''
            assert record[21] == ''
            assert record[22] == ''
            assert record[23] == ''

        if len(record) > 24 and record[1] == 'Kerslake':
            assert record[18] == 'N'
            assert record[19] == ''
            assert record[20] == ''
            assert record[21] == ''
            assert record[22] == ''
            assert record[23] == ''
