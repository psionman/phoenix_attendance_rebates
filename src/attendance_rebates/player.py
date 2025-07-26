"""Player class for Phoenix attendance rebates."""


class Player():
    """Repository for player data."""
    def __init__(self, values: dict):
        self.ebu = values['ebu']
        self.first_name = values['first_name']
        self.surname = values['last_name']
        self.email = values['email']
        self.bbo_username = values['bbo_username']
        self.is_student = values['student']
        self._dollars = 0
        self.bbo_attendance = 0
        self.bbo_qualifying = 0
        self.bbo_bf = 0
        self.bbo_cf = 0
        self.bbo_rebate = 0
        self.f2f_attendance = 0
        self.f2f_qualifying = 0
        self.f2f_bf = 0
        self.f2f_cf = 0
        self.f2f_rebate = 0

    def __repr__(self) -> str:
        return f'{self.ebu} {self.first_name} {self.surname} {self.email}'

    def show_all(self) -> None:
        print('')
        pad = 15
        print(f'{'ebu':<{pad}}{self.ebu}')
        print(f'{'bbo_bf':<{pad}}{self.bbo_bf}')
        print(f'{'bbo_attendance':<{pad}}{self.bbo_attendance}')
        print(f'{'bbo_cf':<{pad}}{self.bbo_cf}')
        print(f'{'bbo_qualifying':<{pad}}{self.bbo_qualifying}')
        print(f'{'bbo_rebate':<{pad}}{self.bbo_rebate}')
        print(f'{'f2f_bf':<{pad}}{self.f2f_bf}')
        print(f'{'f2f_attendance':<{pad}}{self.f2f_attendance}')
        print(f'{'f2f_cf':<{pad}}{self.f2f_cf}')
        print(f'{'f2f_qualifying':<{pad}}{self.f2f_qualifying}')
        print(f'{'f2f_rebate':<{pad}}{self.f2f_rebate}')


def get_players(members: dict[str, object]) -> dict[int, Player]:
    """Return a dict of Player objects."""
    players = {}
    for ebu, member in members.items():
        values = {
            'first_name': member['FIRSTNAME'],
            'last_name': member['SURNAME'],
            'email': member['EMAIL'],
            'ebu': ebu,
            'bbo_username': member['BBOUSERNAME'],
            'student': member['PAYSTATUS'] == '3'
        }
        player = Player(values)
        if ebu and str(ebu).isnumeric():
            players[ebu] = player
    return players
