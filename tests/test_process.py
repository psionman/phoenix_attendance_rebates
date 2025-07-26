"""
Tests for the creation of the f2f and bbo attendance reports,
the f2f payment file and the cf file.
"""

import datetime
from pathlib import Path

from attendance_rebates.rebate_process import RebateProcess
from attendance_rebates.constants import EBU_KEY
from attendance_rebates.csv_utils import get_dict_from_csv_file

from context import rebate_context, test_data_dir

process = RebateProcess(rebate_context)


def test_process_works():
    assert process.create_files() == process.OK
    assert process.f2f_bf == 266
    assert process.f2f_recipients == 45
    assert process.f2f_total == 127.5
    assert process.f2f_cf == 307  # no students!!!

    assert process.bbo_bf == 317
    assert process.bbo_recipients == 48
    assert process.bbo_total == 183
    assert process.bbo_cf == 427


def test_f2f_report():
    path = Path(test_data_dir, 'outputs', 'f2f_att_report_2023_11.csv')
    (f2f_players, fields) = get_dict_from_csv_file(path, EBU_KEY)

    player = f2f_players['403119']
    assert player['Attendance'] == '18'
    assert player['Attendance b/f'] == '9'
    assert player['Attendance c/f'] == '7'
    assert player['EBU'] == '403119'
    assert player['Email'] == 'will.irving@nottingham.ac.uk'
    assert player['First name'] == 'Will'
    assert player['Qualifying attendance'] == '2'
    assert player['Surname'] == 'Irving'
    assert player['rebate'] == '5.00'

    player = f2f_players['423686']
    assert player['Attendance'] == '10'
    assert player['Attendance b/f'] == '2'
    assert player['Attendance c/f'] == '2'
    assert player['EBU'] == '423686'
    assert player['Email'] == 'swharton2491@gmail.com'
    assert player['First name'] == 'Stuart'
    assert player['Qualifying attendance'] == '1'
    assert player['Surname'] == 'Wharton'
    assert player['rebate'] == '2.50'


def test_f2f_rebate_file():
    path = Path(test_data_dir, 'outputs', 'f2f_att_rebate_2023_11.csv')
    with open(path, 'r') as f_rebate:
        rebates = f_rebate.read().split('\n')
    assert len(rebates) == 47
    for rebate in rebates:
        if 'Cumberpatch' in rebate:
            line = rebate.split(',')
            assert line[0] == datetime.datetime.now().strftime('%d-%b-%y')
            assert line[1] == 'CR'
            assert line[3] == '2.50'
            assert line[2] == 'L Cumberpatch PX445622'
        if 'Caldwell' in rebate:
            line = rebate.split(',')
            assert line[0] == datetime.datetime.now().strftime('%d-%b-%y')
            assert line[1] == 'CR'
            assert line[3] == '5.00'
            assert line[2] == 'G Caldwell PX114146'


def test_bbo_report():
    path = Path(test_data_dir, 'outputs', 'bbo_att_report_2023_11.csv')
    (bbo_players, fields) = get_dict_from_csv_file(path, EBU_KEY)

    player = bbo_players['492064']
    assert player['Attendance'] == '18'
    assert player['Attendance b/f'] == '9'
    assert player['Attendance c/f'] == '7'
    assert player['EBU'] == '492064'
    assert player['Email'] == 'jeffwatkins2000@gmail.com'
    assert player['First name'] == 'Jeff'
    assert player['Qualifying attendance'] == '2'
    assert player['Surname'] == 'Watkins'
    assert player['rebate'] == '6.00'

    player = bbo_players['423686']
    assert player['Attendance'] == '6'
    assert player['Attendance b/f'] == '0'
    assert player['Attendance c/f'] == '6'
    assert player['EBU'] == '423686'
    assert player['Email'] == 'swharton2491@gmail.com'
    assert player['First name'] == 'Stuart'
    assert player['Qualifying attendance'] == '0'
    assert player['Surname'] == 'Wharton'
    assert player['rebate'] == '0.00'


def test_cf_file():
    path = Path(test_data_dir, 'outputs', 'cf_2023_11.csv')
    (bbo_players, fields) = get_dict_from_csv_file(path, EBU_KEY)

    player = bbo_players['492064']
    assert player['bbo'] == '7'
    assert player['f2f'] == '0'

    player = bbo_players['423686']
    assert player['bbo'] == '6'
    assert player['f2f'] == '2'

    player = bbo_players['403119']
    assert player['bbo'] == '0'
    assert player['f2f'] == '7'
