from re import match as re_match


class ParsingError(Exception):
    pass


class CommentError(ParsingError):
    pass


def _check_line_format(line: str) -> None:
    if not line.strip() or line[0] == "#":
        raise CommentError("Line is a comment.")

    PATTERN = r"^[^=]+=[^=]+$"
    if not re_match(PATTERN, line):
        raise ParsingError(f"Invalid line format for '{line.strip()}'. "
                           f"Expected format: KEY=value.")


def _check_tuple_format(tuple_str: str) -> None:
    PATTERN = r"^-?\d+,-?\d+$"
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
        "PERFECT": bool,
        "ANIMATIONS": bool,
        "GUI": bool,
        "ALGORITHM": str
    }

    line_splitted = line.split("=")
    if not line_splitted[0] in KEYS_TYPES:
        VALID_KEYS = ', '.join([str(key) for key in KEYS_TYPES.keys()])
        raise ParsingError(f"Invalid key '{line_splitted[0]}' in config line. "
                           f"Valid keys are: {VALID_KEYS}.")
    if KEYS_TYPES[line_splitted[0]] == int:
        try:
            return int(line_splitted[1])
        except ValueError:
            raise ParsingError(f"Invalid value type for '{line.strip()}' "
                               f"in config line. Should be an integer.")
    if KEYS_TYPES[line_splitted[0]] == tuple[int, int]:
        try:
            _check_tuple_format(line_splitted[1])
            value_splitted = line_splitted[1].split(",")
            return (int(value_splitted[0]), int(value_splitted[1]))
        except (ParsingError, ValueError):
            raise ParsingError(f"Invalid tuple format and type for "
                               f"'{line.strip()}'. Expected format: "
                               f"KEY=INT,INT.")
    if KEYS_TYPES[line_splitted[0]] == str:
        if not line_splitted[1].strip():
            raise ParsingError(f"Invalid string value for '{line.strip()}'. "
                               f"Cannot be empty.")
        return line_splitted[1].strip()
    if KEYS_TYPES[line_splitted[0]] == bool:
        try:
            if not (line_splitted[1].strip() == "True"
                    or line_splitted[1].strip() == "False"):
                raise ParsingError(f"Invalid format for '{line.strip()}'. "
                                   "Should be a boolean.")
            return line_splitted[1].strip() == "True"
        except ParsingError:
            raise ParsingError(f"Invalid format for '{line.strip()}'. "
                               f"Should be a boolean.")
    return None


def parse_config(path: str) \
        -> dict[str, int | tuple[int, int] | str | bool | None]:
    with open(path, "r") as f:
        result = {}
        for line in f:
            try:
                _check_line_format(line)
                result[line.split("=")[0]] = _get_line_value(line)
            except CommentError:
                pass
        if "ANIMATIONS" not in result:
            result["ANIMATIONS"] = True
        if "GUI" not in result:
            result["GUI"] = False
        if "ALGORITHM" not in result:
            result["ALGORITHM"] = "DFS"
        algorithm = result.get("ALGORITHM")
        if isinstance(algorithm, str):
            algorithm = algorithm.strip().upper()
            if algorithm not in ("DFS", "KRUSKAL"):
                raise ParsingError(
                    "Invalid ALGORITHM value. Expected DFS or KRUSKAL."
                )
            result["ALGORITHM"] = algorithm

        if result["ENTRY"][0] < 0 or \
                result["ENTRY"][1] < 0 or \
                result["ENTRY"][0] >= result["WIDTH"] or \
                result["ENTRY"][1] >= result["HEIGHT"]:
            raise ParsingError("Entry is out of the grid.")
        if result["EXIT"][0] < 0 or \
                result["EXIT"][1] < 0 or \
                result["EXIT"][0] >= result["WIDTH"] or \
                result["EXIT"][1] >= result["HEIGHT"]:
            raise ParsingError("Exit is out of the grid.")
        return result


def check_config_mandatory(
        config: dict[str, int | tuple[int, int] | str | bool | None]
) -> None:
    for key in ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]:
        if key not in config:
            raise ParsingError(f"Missing mandatory key '{key}' "
                               f"in config file.")