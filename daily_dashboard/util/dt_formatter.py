def strftime_date_format(f, platform, include_year=False):
    """
    Generate and return a strftime friendly formatting string

    :param f: One of three styles:
        'MDY': January 1 2020
        'DMY': 1 January 2020
        'YMD': 2020 January 1
    :param platform: The platform from which the request was sent
    :param include_year: A boolean for including the year
    :return: A strftime friendly formatting string
    """
    pf_specific_ch = '#' if platform == 'windows' else '-'

    day = f'%{pf_specific_ch}d'
    month = '%B'
    year = '%Y' if include_year else ''

    if f == 'DMY':
        res = f'{day} {month} {year}'
    elif f == 'YMD':
        res = f'{year} {month} {day}'
    else:
        res = f'{month} {day} {year}'

    return res.strip()


def strftime_time_format(hr24, platform):
    if hr24:
        return '%H:%M'

    pf_specific_ch = '#' if platform == 'windows' else '-'
    return f'%{pf_specific_ch}I:%M %p'
