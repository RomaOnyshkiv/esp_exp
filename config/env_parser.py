COMMENT_PREFIX = "#"
EXPORT_PREFIX = "export "
KEY_VALUE_SEPARATOR = "="
QUOTE_CHARS = ('"', "'")
INLINE_COMMENT_MARKER = " #"


class EnvParseError(Exception):
    pass


def parse_line(raw_line, line_number):
    line = raw_line.strip()
    if not line or line.startswith(COMMENT_PREFIX):
        return None

    if line.startswith(EXPORT_PREFIX):
        line = line[len(EXPORT_PREFIX):].strip()

    if KEY_VALUE_SEPARATOR not in line:
        raise EnvParseError("Line {}: missing '='".format(line_number))

    key, value = line.split(KEY_VALUE_SEPARATOR, 1)
    key = key.strip()
    if not key:
        raise EnvParseError("Line {}: empty key".format(line_number))

    return key, _clean_value(value.strip())


def _clean_value(value):
    # Значення в лапках беремо як є (разом з # всередині, напр. паролі).
    if len(value) >= 2 and value[0] in QUOTE_CHARS and value[-1] == value[0]:
        return value[1:-1]
    # Для значень без лапок відрізаємо inline-коментар: KEY=value  # comment
    marker_index = value.find(INLINE_COMMENT_MARKER)
    if marker_index != -1:
        value = value[:marker_index]
    return value.strip()