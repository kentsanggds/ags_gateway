def in_colour(msg, fg, bg=None):
    return '\x1b[0;{}{}m{}\x1b[0m'.format(fg, (';' + bg if bg else ''), msg)


def notify(msg):
    print(in_colour(msg, 37))


def status_ok(msg):
    print(in_colour(msg, 32))


def status_ok_info(msg):
    print(in_colour(msg, 34))


def status_err(msg):
    print(in_colour(msg, 31))
