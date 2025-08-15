"""
    Perform rebate calculations and generate
    attendance reports, payment file and cf file.
"""

import datetime
import csv
from collections import namedtuple

from psiutils.utilities import logger

from attendance_rebates.config import get_config
from attendance_rebates.player import Player, get_players
from attendance_rebates.constants import (
    REPORT_FIELDS, SHOW_ALL_RECORDS, EBU_KEY)
from attendance_rebates.csv_utils import get_dict_from_csv_file, write_csv_file

Context = namedtuple(
    'Context', (
        'period_start',
        'period_end',
        'membership_file',
        'f2f_input_file',
        'f2f_report_file',
        'f2f_rebate_file',
        'bbo_input_file',
        'bbo_report_file',
        'bbo_rebate_file',
        'cf_input_file',
        'cf_output_file',
        )
    )


class RebateProcess():
    def __init__(self, context):
        config = get_config()
        # Dates
        self.payment_months = config.payment_months
        self.start_date = context.period_start.date()
        self.latest_date = context.period_end.date()

        # Rebate
        self.qualifying_attendances = config.qualifying_attendances
        self.rebate_f2f = config.rebate_f2f
        self.rebate_bbo = config.rebate_bbo

        # Files
        self.membership_file = context.membership_file
        self.f2f_input_file = context.f2f_input_file
        self.f2f_report_file = context.f2f_report_file
        self.f2f_rebate_file = context.f2f_rebate_file
        self.bbo_input_file = context.bbo_input_file
        self.bbo_report_file = context.bbo_report_file
        self.bbo_rebate_file = context.bbo_rebate_file
        self.cf_input_file = context.cf_input_file
        self.cf_output_file = context.cf_output_file

        # Totals
        self.f2f_bf = 0
        self.f2f_recipients = 0
        self.f2f_total = 0
        self.f2f_cf = 0

        self.bbo_bf = 0
        self.bbo_recipients = 0
        self.bbo_total = 0
        self.bbo_cf = 0

        self.OK = 1

    def create_files(self) -> None:
        """Control calculations and output."""
        logger.info(
            "Starting rebate process",
            period_start=self.start_date,
            period_end=self.latest_date,
        )
        (members, members_fields) = get_dict_from_csv_file(
            self.membership_file,
            EBU_KEY
            )
        logger.info(
            "Retrieved membership data",
            path=str(self.membership_file)
        )
        del members_fields
        (cf_data, cf_fields) = get_dict_from_csv_file(
            self.cf_input_file,
            EBU_KEY
            )
        logger.info(
            "Retrieved carried forward data",
            path=str(self.cf_input_file)
        )
        players = get_players(members)
        self.update_player_bf(players, cf_data)
        self.update_format_attendance(players, self.f2f_input_file, 'f2f')
        self.update_format_attendance(players, self.bbo_input_file, 'bbo')

        self.calculate_player_rebate(players)

        # Create cf file
        self._create_cf_output_file(players, cf_fields)

        # Reports
        self._generate_bbo_report(players)
        self._generate_bbo_output(players)
        self._generate_f2f_report(players)
        self._generate_f2f_payment_file(players)

        # Wrap up
        logger.info("Rebate process complete", stage="end", status="success")
        return self.OK

    def _generate_bbo_report(self, players: dict[int: Player]) -> None:
        """Create an output report for BBO."""
        report_path = self.bbo_report_file
        try:
            with open(report_path, mode='w', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=REPORT_FIELDS)
                self._write_bbo_report(writer, players)

            logger.info(
                'Generated BBO report file',
                path=str(report_path),
                recipients=self.bbo_recipients,
                total_amount=f'${self.bbo_total:.2f}',
            )
        except FileExistsError:
            logger.exception(f'Failed to write {report_path}')

    def _write_bbo_report(self, writer: object, players: dict) -> None:
        writer.writeheader()

        for player in players.values():
            if ((player.bbo_rebate +
                player.bbo_bf +
                player.bbo_attendance) > 0
                    or SHOW_ALL_RECORDS):
                output = self._get_output_for_bbo_player(player)
                writer.writerow(output)

    def _get_output_for_bbo_player(self, player):
        if player.bbo_rebate:
            self.bbo_recipients += 1
        self.bbo_bf += player.bbo_bf
        self.bbo_total += player.bbo_rebate
        self.bbo_cf += player.bbo_cf
        return {
            'EBU': player.ebu,
            'First name': player.first_name,
            'Surname': player.surname,
            'Email': player.email,
            'Attendance b/f': player.bbo_bf,
            'Attendance': player.bbo_attendance,
            'Qualifying attendance': player.bbo_qualifying,
            'Attendance c/f': player.bbo_cf,
            'rebate': f'{player.bbo_rebate:.2f}'
        }

    def _generate_bbo_output(self, players: dict[int: Player]) -> None:
        """Create an output file for BBO."""
        report_path = self.bbo_rebate_file
        try:
            with open(report_path, mode='w', encoding='utf-8') as csv_file:
                fieldnames = ['BBO username', 'Amount']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                self._write_bbo_output(writer, players)

            logger.info(
                "Generated BBO rebate file",
                path=str(report_path),
                recipients=self.bbo_recipients,
                total_amount=f'${self.bbo_total:.2f}',
            )
        except FileExistsError:
            logger.exception(f'Failed to write {report_path}')

    def _write_bbo_output(self, writer: object, players: dict) -> None:
        writer.writeheader()

        for player in players.values():
            if player.bbo_rebate:
                writer.writerow({
                    'BBO username': player.bbo_username,
                    'Amount': player.bbo_rebate,
                })

    def _generate_f2f_report(self, players: dict) -> None:
        """Create an output report for F2F."""
        report_path = self.f2f_report_file
        try:
            with open(report_path, mode='w', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=REPORT_FIELDS)
                self._write_f2f_report(writer, players)

            logger.info(
                "Generated F2F rebate file",
                path=str(report_path),
                recipients=self.f2f_recipients,
                total_amount=f'£{self.f2f_total:.2f}',
            )
        except FileExistsError:
            logger.exception(f'Failed to write {report_path}')

    def _write_f2f_report(self, writer: object, players: dict) -> None:
        writer.writeheader()

        for player in players.values():
            if player.is_student:
                continue

            if ((player.f2f_rebate
                    + player.f2f_bf
                    + player.f2f_attendance) > 0
                    or SHOW_ALL_RECORDS):
                output = self._get_output_for_f2f_player(player)
                writer.writerow(output)

    def _get_output_for_f2f_player(self, player):
        if player.f2f_rebate:
            self.f2f_recipients += 1
        self.f2f_bf += player.f2f_bf
        self.f2f_total += player.f2f_rebate
        self.f2f_cf += player.f2f_cf
        return {
            'EBU': player.ebu,
            'First name': player.first_name,
            'Surname': player.surname,
            'Email': player.email,
            'Attendance b/f': player.f2f_bf,
            'Attendance': player.f2f_attendance,
            'Qualifying attendance': player.f2f_qualifying,
            'Attendance c/f': player.f2f_cf,
            'rebate': f'{player.f2f_rebate:.2f}'
        }

    def _generate_f2f_payment_file(self, players: dict[int: Player]) -> None:
        """Create an output file for F2F."""
        report_path = self.f2f_rebate_file
        fieldnames = ['Date', 'Type', 'Description', 'Amount']
        with open(report_path, mode='w', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            self._write_f2f_payment_file(writer, players)

            logger.info(
                "Generated F2F report file",
                path=str(report_path),
                recipients=self.f2f_recipients,
                total_amount=f'£{self.f2f_total:.2f}',
            )

    def _write_f2f_payment_file(self, writer: object, players: dict) -> None:
        writer.writeheader()

        for player in players.values():
            if player.is_student:
                continue
            if player.f2f_rebate:
                output = self._generate_player_data_for_f2f_payment_file(
                    player
                    )
                writer.writerow(output)

    def _generate_player_data_for_f2f_payment_file(self, player):
        return {
            'Date': datetime.datetime.now().strftime('%d-%b-%y'),
            'Type': 'CR',
            'Description': (f'{player.first_name[0]} '
                            f'{player.surname} PX{player.ebu}'),
            'Amount': f'{player.f2f_rebate:.2f}',
        }

    def _create_cf_output_file(self, players, cf_fields):
        # Create a file of carried forward data
        report_path = self.cf_output_file
        cf_items = {
            player.ebu: {
                'EBU': player.ebu,
                'bbo': player.bbo_cf,
                'f2f': player.f2f_cf,
            }
            for player in players.values()
            if player.f2f_cf or player.bbo_cf
        }
        write_csv_file(report_path, cf_fields, cf_items)
        logger.info(
            "CF output file generated",
            stage="cf_output",
            file_path=report_path,
            records=len(cf_items),
        )

    def calculate_player_rebate(self, players: dict[int: Player]) -> None:
        """Process a player."""
        qualifying_attendances = self.qualifying_attendances

        for player in players.values():
            aggregate_attendance = player.bbo_attendance + player.bbo_bf
            player.bbo_qualifying = int(
                aggregate_attendance / qualifying_attendances
                )
            player.bbo_cf = aggregate_attendance % qualifying_attendances
            player.bbo_rebate = player.bbo_qualifying * self.rebate_bbo / 100

            aggregate_attendance = player.f2f_attendance + player.f2f_bf
            player.f2f_qualifying = int(
                aggregate_attendance / qualifying_attendances
                )
            player.f2f_cf = aggregate_attendance % qualifying_attendances
            player.f2f_rebate = player.f2f_qualifying * self.rebate_f2f / 100

    def update_format_attendance(self,
                                 players: dict[int: Player],
                                 path: str,
                                 format: str) -> None:
        """Process attendance for relevant format."""
        (att_data, att_fields) = get_dict_from_csv_file(path, EBU_KEY)
        for ebu, att_item in att_data.items():
            if ebu in players:
                player = players[ebu]
                for raw_date, attendance in att_item.items():
                    attendance_date = self._get_attendance_date(raw_date)
                    self._update_players_attendance(
                        player,
                        format,
                        attendance,
                        attendance_date
                        )

    def _update_players_attendance(
            self,
            player: Player,
            format: str,
            attendance: int,
            attendance_date: datetime) -> None:
        if (self.start_date <= attendance_date <= self.latest_date
                and attendance.isnumeric()):
            if format == 'bbo':
                player.bbo_attendance += int(attendance)
            elif format == 'f2f':
                player.f2f_attendance += int(attendance)

    def _get_attendance_date(self, raw_date):
        if '/' not in raw_date:
            return datetime.date(1900, 1, 1)
        month_year = raw_date.split('/')
        month = int(month_year[0])
        year = 2000 + int(month_year[1])
        return datetime.date(year=year, month=month, day=1)

    def update_player_bf(self, players: dict[int: Player],
                         cf_data: dict[str, object]) -> None:
        """Update players with carried forward from last period."""
        for ebu, cf_info in cf_data.items():
            if not str(ebu).isnumeric():
                continue
            if ebu in players:
                player = players[ebu]
                player.bbo_bf = int(cf_info['bbo'])
                player.f2f_bf = int(cf_info['f2f'])
