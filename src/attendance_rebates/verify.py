"""
    Verify that all transaction cf and bf details match.

    There are 4 verifications

        1. players
        2. bbo rebates
        3. f2f rebates
        4. bf/cf values

    The
"""

import sys
from datetime import datetime
import dateutil.relativedelta
from pathlib import Path
# from termcolor import cprint

from player import Player as PlayerMaster
from constants import EBU_KEY, BBO_KEY, INFO_COLOUR, YYYYMM, USER_DATA_DIR
from csv_utils import get_dict_from_csv_file
from session import Session

START_DATE = datetime(2023, 8, 1)
FORMATS = ['bbo', 'f2f']
REPORT_NAME = 'att_report'
REBATE_NAME = 'att_rebate'
QUALIFIED = 10

TEST_MEMBER = '492064'
TEST_MEMBER = None


class Player(PlayerMaster):
    def __init__(self, values: dict, dates: int):
        super().__init__(values)
        self.bbo_bf_transactions = [0 for date in range(dates)]
        self.bbo_attendance_transactions = [0 for date in range(dates)]
        self.bbo_cf_transactions = [0 for date in range(dates)]
        self.bbo_rebate_transactions = [0 for date in range(dates)]

        self.f2f_bf_transactions = [0 for date in range(dates)]
        self.f2f_attendance_transactions = [0 for date in range(dates)]
        self.f2f_cf_transactions = [0 for date in range(dates)]
        self.f2f_rebate_transactions = [0 for date in range(dates)]

    def show_bbo(self) -> None:
        print(f'{self.ebu=}')
        print(f'{self.bbo_bf_transactions=}')
        print(f'{self.bbo_attendance_transactions=}')
        print(f'{self.bbo_cf_transactions=}')
        print(f'{self.bbo_rebate_transactions=}')

    def show_f2f(self) -> None:
        print(f'{self.ebu=}')
        print(f'{self.f2f_bf_transactions=}')
        print(f'{self.f2f_attendance_transactions=}')
        print(f'{self.f2f_cf_transactions=}')
        print(f'{self.f2f_rebate_transactions=}')


def verification(session: Session, ebu: str = '') -> bool:
    dates = _get_dates()
    # files = _get_files(session)

    players = _get_players(session.membership_file, dates)
    if not players:
        return False

    result = _verify_players(players)
    if not result:
        return False

    result = _verify_rebates(players, dates)
    if not result:
        return False

    if ebu and not TEST_MEMBER:
        if ebu not in players:
            return f'Invalid EBU number: {ebu}'

        player = players[ebu]
        return _print_detail(player, dates)
    return True


def _verify_players(members: dict) -> None:
    for member in members.values():
        for index in range(len(member.bbo_bf_transactions) - 1):
            _verify_bbo_cf(member, index)
            _verify_f2f_cf(member, index)

        for index in range(len(member.bbo_bf_transactions)):
            _verify_bbo_arithmetic(member, index)
            _verify_f2f_arithmetic(member, index)
    return True


def _verify_bbo_cf(member: Player, index: int) -> None:
    # Verify the the BBO cf values match
    bf = member.bbo_bf_transactions[index+1]
    cf = member.bbo_cf_transactions[index]
    if bf != cf:
        raise ValueError((f'bbo_bf: {index=}, {member} \n'
                          f'{member.bbo_bf_transactions=} \n'
                          f'{member.bbo_cf_transactions=}'))


def _verify_f2f_cf(member: Player, index: int) -> None:
    # Verify the the F2F cf values match
    bf = member.f2f_bf_transactions[index+1]
    cf = member.f2f_cf_transactions[index]
    if bf != cf:
        raise ValueError((f'f2f_bf: {index=}, {member} \n'
                          f'{member.f2f_bf_transactions=} \n'
                          f'{member.f2f_cf_transactions=}'))


def _verify_bbo_arithmetic(member: Player, index: int) -> None:
    bf = member.bbo_bf_transactions[index]
    att = member.bbo_attendance_transactions[index]
    cf = member.bbo_cf_transactions[index]
    used = (int((bf + att) / QUALIFIED)) * QUALIFIED
    if bf + att - used != cf:
        raise ValueError(f'bbo balance: {index=}, {member}')
    remainder = (bf + att) % QUALIFIED
    if cf != remainder:
        raise ValueError(f'bbo remainder: {index=}, {member}')


def _verify_f2f_arithmetic(member: Player, index: int) -> None:
    bf = member.f2f_bf_transactions[index]
    att = member.f2f_attendance_transactions[index]
    cf = member.f2f_cf_transactions[index]
    used = (int((bf + att) / QUALIFIED)) * QUALIFIED
    if bf + att - used != cf:
        raise ValueError(f'bbo balance: {index=}, {member}')
    remainder = (bf + att) % QUALIFIED
    if cf != remainder:
        raise ValueError(f'f2f remainder: {index=}, {member}')


def _verify_rebates(players: dict, dates: list) -> bool:
    for index, date in enumerate(dates):
        result = _verify_bbo_rebate_file(players, index, date)
        if not result:
            return False

        result = _verify_f2f_rebate_file(players, index, date)
        if not result:
            return False

        # Compare the cf file with the values held in the relevant att-report
        result = _verify_cf_file(players, index, date)
        if not result:
            return False
    return True


def _verify_bbo_rebate_file(
        players: dict,
        index: int,
        date: str,
        ) -> bool:
    players = {player.bbo_username: player for player in players.values()}
    path = Path(USER_DATA_DIR, date, f'bbo_{REBATE_NAME}_{date}.csv')
    (records, members_fields) = get_dict_from_csv_file(path, BBO_KEY)

    for record in records.values():
        if record['BBO username'] == BBO_KEY:
            continue
        if record['BBO username'] not in players:
            continue
        player = players[record['BBO username']]
        rebate_value = player.bbo_rebate_transactions[index]
        if float(record['Amount']) != float(rebate_value):
            raise ValueError(
                f"bbo_rebate error {date} {record['BBO username']}"
            )
    return True


def _verify_f2f_rebate_file(
        players: dict,
        index: int,
        date: str,
        ) -> bool:
    path = Path(USER_DATA_DIR, date, f'f2f_{REBATE_NAME}_{date}.csv')
    (records, members_fields) = get_dict_from_csv_file(path, 'Description')
    for record in records.values():
        description = record['Description']
        pos = description.find('PX')
        ebu = description[pos+2:]
        if record['Description'] == 'Description':
            continue
        if ebu not in players:
            continue
        player = players[ebu]
        rebate_value = player.f2f_rebate_transactions[index]
        if float(record['Amount']) != float(rebate_value):
            raise ValueError(f'f2f_rebate error {date} {ebu}')
    return True


def _verify_cf_file(
        players: dict,
        index: int,
        date: str,
        ) -> bool:
    path = Path(USER_DATA_DIR, date, f'cf_{date}.csv')
    (records, members_fields) = get_dict_from_csv_file(path, EBU_KEY)
    for ebu, record in records.items():
        if record['EBU'] == 'EBU':
            continue
        if ebu not in players:
            continue
        player = players[ebu]
        _verify_bbo_cf_file(record,  player, date, index)
        _verify_f2f_cf_file(record,  player, date, index)
    return True


def _verify_bbo_cf_file(record: dict, player: Player,
                        date: str, index: int) -> None:
    if not player.bbo_rebate:
        return
    player_bbo_cf = player.bbo_cf_transactions[index]
    if int(record['bbo']) != player_bbo_cf:
        raise ValueError(f'bbo_cf error {date=} {player.ebu=} '
                         f'{int(record["bbo"])=} '
                         f'{player_bbo_cf=}')


def _verify_f2f_cf_file(record: dict, player: Player,
                        date: str, index: int) -> None:
    if not player.f2f_rebate:
        return
    player_f2f_cf = player.f2f_cf_transactions[index]
    if int(record['f2f']) != player_f2f_cf:
        ic(int(record['f2f']), player_f2f_cf)
        player.show_f2f()
        raise ValueError(f'f2f_cf error {date=} {player.ebu=} '
                         f'{int(record["f2f"])=} '
                         f'{player_f2f_cf=}')


def _print_detail(player: Player, dates: list) -> None:
    # Print out the details fro the nominated member
    output = []
    output.append(f'Player: {player.ebu} {player.first_name} {player.surname}')
    output.append(f'BBO {"-" * 40}')
    output.append((f'{"Date":<8}{"b/f":>4}{"Att":>6}{"qual":>6}'
                   f'{"used":>6}{"c/f":>6}{"paid":>7}'))
    # _print_heading()
    for index, date in enumerate(dates):
        bf = player.bbo_bf_transactions[index]
        att = player.bbo_attendance_transactions[index]
        qualified = bf + att
        used = int(qualified / QUALIFIED) * QUALIFIED
        cf = player.bbo_cf_transactions[index]
        paid = player.bbo_rebate_transactions[index]
        if paid == '':
            paid = 0
        paid = int(float(paid))
        output.append(
            (f'{date:<8}{bf:>4}{att:>6}{qualified:>6}{used:>6}{cf:>6}'
             f'{paid:>7.2f}'))

    output.append('')
    output.append(f'F2F {"-" * 40}')
    output.append((f'{"Date":<8}{"b/f":>4}{"Att":>6}{"qual":>6}'
                   f'{"used":>6}{"c/f":>6}{"paid":>7}'))
    for index, date in enumerate(dates):
        bf = player.f2f_bf_transactions[index]
        att = player.f2f_attendance_transactions[index]
        qualified = bf + att
        used = int(qualified / QUALIFIED) * QUALIFIED
        cf = player.f2f_cf_transactions[index]
        paid = player.f2f_rebate_transactions[index]
        if paid == '':
            paid = 0
        paid = float(paid)
        output.append(
            (f'{date:<8}{bf:>4}{att:>6}{qualified:>6}{used:>6}{cf:>6}'
             f'{paid:>7.2f}'))
    return output


def _get_dates() -> list[str]:
    # return a list of dates stating with START_DATE
    dates = []
    period = 0
    while True:
        file_date = START_DATE + dateutil.relativedelta.relativedelta(
            months=3*period
            )
        dates.append(file_date.strftime(YYYYMM))
        if file_date > datetime.now():
            break
        period += 1
    return dates[:-1]


def _get_players(members_file: str, dates: list) -> dict[str, Player]:
    # Return a dict of Player objects keyed on ebu number

    # Get a dict of players from the members files
    path = Path(Path.home(), 'Downloads', members_file)
    players = _read_players(path, len(dates))

    # For each date get the *att* files and update players with the
    # transactions
    for index, date in enumerate(dates):
        for mode in FORMATS:
            path = Path(USER_DATA_DIR, date, f'{mode}_{REPORT_NAME}_{date}.csv')
            _update_players(path, mode, index, players)

    if TEST_MEMBER:
        players = {TEST_MEMBER: players[TEST_MEMBER]}
    return players


def _read_players(file: Path, number_of_dates: int) -> dict[str, Player]:
    # Return a dict of players
    players = {}
    (members, members_fields) = get_dict_from_csv_file(file, EBU_KEY)
    for ebu, member in members.items():
        values = {
            'first_name': member['FIRSTNAME'],
            'last_name': member['SURNAME'],
            'email': member['EMAIL'],
            'ebu': ebu,
            'bbo_username': member['BBOUSERNAME'],
            'student': member['PAYSTATUS'] == '3'}

        player = Player(values, number_of_dates)
        if member['PAYSTATUS'] == '3':
            continue
        players[player.ebu] = player
    return players


def _update_players(
        path: Path,
        mode: str,
        index: int,
        players: dict[str, Player]) -> None:

    # Files are xxx_att_report_yyyymm.csv
    # Create a transaction dict and apply to every player
    (transactions, members_fields) = get_dict_from_csv_file(path, EBU_KEY)

    # members_fields
    # ['EBU',
    # 'First name',
    # 'Surname',
    # 'Email',
    # 'Attendance b/f',
    # 'Attendance',
    # 'Qualifying attendance',
    # 'Attendance c/f',
    # 'rebate']

    # Add an index to the transaction
    for transaction in transactions.values():
        transaction['index'] = index

    # Update the player with the values
    missing = []
    for ebu, transaction in transactions.items():
        if transaction['EBU'] == 'EBU':
            continue
        if ebu not in players:
            missing.append(ebu)
            continue

        member = players[transaction['EBU']]
        _update_player(member, transaction, mode, index)


def _update_player(member: Player, transaction: dict, mode: str, index: int):
    # Apply the transactions to the player transaction attributes
    if mode == 'bbo':
        member.bbo_bf_transactions[index] = int(transaction['Attendance b/f'])
        member.bbo_attendance_transactions[index] = int(
            transaction['Attendance'])
        member.bbo_cf_transactions[index] = int(transaction['Attendance c/f'])
        member.bbo_rebate_transactions[index] = transaction['rebate']

    if mode == 'f2f':
        member.f2f_bf_transactions[index] = int(transaction['Attendance b/f'])
        member.f2f_attendance_transactions[index] = int(
            transaction['Attendance'])
        member.f2f_cf_transactions[index] = int(transaction['Attendance c/f'])
        member.f2f_rebate_transactions[index] = transaction['rebate']

    if member.ebu == TEST_MEMBER:
        ic(member.bbo_bf_transactions)
        ic(member.bbo_cf_transactions)


if __name__ == '__main__':
    ebu = ''
    if len(sys.argv) > 1:
        ebu = sys.argv[1]
    verification(ebu)
    print('Done ...')
