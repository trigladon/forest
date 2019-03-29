import re


def common_parser(format, message):
    r = re.search(format, message)
    result = r.groupdict() if r else {}
    return result


def parse_message(format, message):
    return common_parser(format, message)


def to_number(number):
    if number:
        try:
            t_number = number.replace(' ', '')
        except AttributeError:
            t_number = number
        try:
            return int(t_number)
        except ValueError:
            try:
                return float(t_number)
            except ValueError:
                return number
    return number
