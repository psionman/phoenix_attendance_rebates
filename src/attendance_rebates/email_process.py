"""Create email and reset files for upload to Bridgewebs."""

from collections import namedtuple

from attendance_rebates.config import get_config
from attendance_rebates.csv_utils import get_dict_from_csv_file, write_csv_file
import attendance_rebates.text as text


Context = namedtuple(
    'Context',
    (
        'period_date',
        'membership_file',
        'input_file',
        'output_file',
        'bbo_payment_file',
        )
)


class EmailProcess():
    """
    Use the email_input_file to update the membership_file,
    creating email_output_file and the email_reset_file.
    The Bridgewebs database has the fields in BRIDGEWEBS_XREF
    """
    def __init__(self, context: namedtuple,) -> None:
        config = get_config()
        self.context = context
        # Dates
        self.period_date = context.period_date

        # Files
        self.membership_file = context.membership_file
        self.email_input_file = context.input_file
        self.email_output_file = context.output_file
        self.email_reset_file = str(self.email_output_file).replace(
            text.EMAIL, text.RESET)
        self.bbo_payment_file = ''

        # Email attributes
        self.email_flag_club = f'{text.CLUB}{config.email_flag_club}'
        self.rebate_club = f'{text.CLUB}{config.rebate_club}'
        self.brought_forward_club = f'{text.CLUB}{config.brought_forward_club}'
        self.sessions_club = f'{text.CLUB}{config.sessions_club}'
        self.carried_forward_club = f'{text.CLUB}{config.carried_forward_club}'
        self.quarter_club = f'{text.CLUB}{config.quarter_club}'

        self.OK = 1

    def create_files(self) -> None:
        """ Create the output files."""
        (members, members_fields) = get_dict_from_csv_file(
            self.membership_file,
            'EBU'
            )
        (rebates, rebate_fields) = get_dict_from_csv_file(
            self.email_input_file,
            'EBU'
            )

        rebate_members = self._get_members_with_rebate(members, rebates)
        if self.context.bbo_payment_file:
            self._create_bbo_payment_file(rebate_members)
        email_ok = self._write_email_file(members_fields, rebate_members)

        reset_members = self._get_reset_records(rebate_members)
        reset_ok = self._write_reset_file(members_fields, reset_members)
        if email_ok and reset_ok:
            return self.OK
        return False

    def _write_email_file(self, members_fields, rebate_members):
        # Write email file
        try:
            write_csv_file(
                self.email_output_file,
                members_fields,
                rebate_members
                )
            return True
        except FileNotFoundError:
            return False

    def _write_reset_file(self, members_fields, reset_members):
        # Write reset file
        try:
            write_csv_file(
                self.email_reset_file,
                members_fields,
                reset_members
                )
            return True
        except FileNotFoundError:
            return False

    def _create_bbo_payment_file(self, members) -> None:
        payments = [(member['BBOUSERNAME'], member['CLUB6'])
                    for member in members. values()]
        payments.sort(key=lambda item: item[0])
        payments.sort(key=lambda item: item[1])

        output = [f'{item[0]}, {item[1]}' for item in payments]

        path = self.context.bbo_payment_file
        with open(path, 'w', encoding='utf-8') as f_payments:
            f_payments.write('\n'.join(output))

    def _get_members_with_rebate(self, members, rebates):
        rebate_members = {}
        for key, rebate in rebates.items():
            try:
                if float(rebate['rebate']) > 0:
                    rebate_members[key] = self._get_member_record(
                        members,
                        key,
                        rebate
                        )
            except ValueError:
                pass
        return rebate_members

    def _get_member_record(
            self,
            members: list[dict],
            key: str,
            rebate: dict
            ) -> list[str]:
        attendance_bf = self._swap_zero(rebate['Attendance b/f'])
        attendance = self._swap_zero(rebate['Attendance'])
        attendance_cf = self._swap_zero(rebate['Attendance c/f'])
        member = members[key]
        member[self.email_flag_club] = 'Y'
        member[self.rebate_club] = f"{float(rebate['rebate']):.2f}"
        member[self.brought_forward_club] = f"{attendance_bf}"
        member[self.sessions_club] = f"{attendance}"
        member[self.carried_forward_club] = f"{attendance_cf}"
        member[self.quarter_club] = f"{self.period_date}"
        return member

    def _get_reset_records(self, rebate_members) -> list[str]:
        for member in rebate_members.values():
            member[self.email_flag_club] = 'N'
            member[self.rebate_club] = ''
            member[self.brought_forward_club] = ''
            member[self.sessions_club] = ''
            member[self.carried_forward_club] = ''
            member[self.quarter_club] = ''
        return rebate_members

    def _swap_zero(self, text: str) -> str:
        if int(text) == 0:
            return 'Zero'
        return text
