from config.env_parser import parse_line

ENV_FILE_PATH = "/.env"
TRUE_VALUES = ("1", "true", "yes", "on")
FALSE_VALUES = ("0", "false", "no", "off")


class ConfigError(Exception):
    pass


class ConfigReader:

    _values = None

    @classmethod
    def load(cls, path=ENV_FILE_PATH):
        values = {}
        try:
            with open(path) as env_file:
                line_number = 0
                while True:
                    raw_line = env_file.readline()
                    if not raw_line:
                        break
                    line_number += 1
                    parsed = parse_line(raw_line, line_number)
                    if parsed:
                        values[parsed[0]] = parsed[1]
        except OSError as error:
            raise ConfigError("Cannot open env file {}: {}".format(path, error))
        cls._values = values

    @classmethod
    def get(cls, key, default=None):
        if cls._values is None:
            cls.load()
        value = cls._values.get(key, default)
        if value is None:
            raise ConfigError("Config key not found: {}".format(key))
        return value

    @classmethod
    def get_int(cls, key, default=None):
        raw = cls.get(key, None if default is None else str(default))
        try:
            return int(raw)
        except ValueError:
            raise ConfigError("Config key {} is not an int: {}".format(key, raw))

    @classmethod
    def get_bool(cls, key, default=None):
        raw = cls.get(key, None if default is None else str(default)).lower()
        if raw in TRUE_VALUES:
            return True
        if raw in FALSE_VALUES:
            return False
        raise ConfigError("Config key {} is not a bool: {}".format(key, raw))