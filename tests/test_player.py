from attendance_rebates.player import Player


def test_Player_repr():
    data = {
        'ebu': '123456',
        'first_name': 'fred',
        'last_name': 'bloggs',
        'email': '',
        'bbo_username': '',
        'student': '',
    }
    player = Player(data)
    assert repr(player) == '123456 fred bloggs ' # note space for email!
