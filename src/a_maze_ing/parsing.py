from re import match as re_match


class ParsingError(Exception):
    pass


def _check_line_format(line: str) -> None:
    PATTERN = r"^[^=]+=[^=]+$"
    if not re_match(PATTERN, line):
        raise ParsingError("Invalid line format. Expected format: KEY=value.")


def _check_tuple_format(tuple_str: str) -> None:
    PATTERN = r"^\d+,\d+$"
    if not re_match(PATTERN, tuple_str.strip()):
        raise ParsingError(
            f"Invalid tuple format: '{tuple_str}'. Expected format: INT,INT.")


def _get_line_value(line: str) -> int | tuple[int, int] | str | bool | None:
    KEYS_TYPES: dict[str, type] = {
        "WIDTH": int,
        "HEIGHT": int,
        "ENTRY": tuple[int, int],
        "EXIT": tuple[int, int],
        "OUTPUT_FILE": str,
        "PERFECT": bool
    }

    line_splitted = line.split("=")
    if not line_splitted[0] in KEYS_TYPES:
        raise ParsingError(f"Invalid key in config line. Valid keys are: "
                           f"{", ".join(
                               [str(key) for key in KEYS_TYPES.keys()]
                           )}.")
    if KEYS_TYPES[line_splitted[0]] == int:
        try:
            return int(line_splitted[1])
        except ValueError:
            raise ParsingError(f"Invalid value type for '{line_splitted[0]}' "
                               f"in config line. Should be an integer.")
    if KEYS_TYPES[line_splitted[0]] == tuple[int, int]:
        try:
            _check_tuple_format(line_splitted[1])
            value_splitted = line_splitted[1].split(",")
            return (int(value_splitted[0]), int(value_splitted[1]))
        except (ParsingError, ValueError):
            raise ParsingError("Invalid tuple format and type. "
                               "Expected format: INT,INT.")
    if KEYS_TYPES[line_splitted[0]] == str:
        if not line_splitted[1].strip():
            raise ParsingError("Invalid string value. Cannot be empty.")
        return line_splitted[1].strip()
    if KEYS_TYPES[line_splitted[0]] == bool:
        try:
            if not (line_splitted[1].strip() == "True"
                    or line_splitted[1].strip() == "False"):
                raise ParsingError("Invalid boolean format. "
                                   "Should be a boolean.")
            return line_splitted[1].strip() == "True"
        except ParsingError:
            raise ParsingError("Invalid boolean format. Should be a boolean.")
    return None


def parse_config(path: str) -> (
        dict[str, int | tuple[int, int] | str | bool | None] | None
):
    with open(path, "r") as f:
        try:
            result = {}
            for line in f:
                _check_line_format(line)
                result[line.split("=")[0]] = _get_line_value(line)
            return result
        except ParsingError as e:
            print(e)
    return None
