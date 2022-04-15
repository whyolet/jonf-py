"""JONF parser/formatter in Python - https://jonf.app/"""

__version__ = "0.0.6"
__jonf_format_version__ = "0.0.13"

import json
from typing import Any, Callable, Tuple

BASIC_TYPES = (bool, int, float, str)
ARRAYS = (list, tuple)
OBJECTS = (dict,)
COLLECTIONS = ARRAYS + OBJECTS
EMPTIES: Tuple[Any, Any, Any, Any] = ("", [], (), {})
INDENT = "  "
SPACES = " \t\r\n"
INNER_COMMENT_MARKS = tuple(space + "#" for space in SPACES)
OBJECT_KEY_MARKS_TO_QUOTE = SPACES + '"-='


def parse(text: str, json_parse: Callable[[str], Any] = json.loads) -> Any:
    """Parses JONF text to Python data

    Args:
        text: JONF text
        json_parse: JSON parser to use, default is `json.loads`

    Returns:
        Python data, parsed from this text

    Example::

        text = textwrap.dedent(
            '''\
            compare =
              - true
              = true
            '''
        ).rstrip()

        assert jonf.parse(text) == {"compare": ["true", True]}
    """
    raise NotImplementedError


def format(data: Any, json_format: Callable[[Any], str] = json.dumps) -> str:
    """Formats Python data to JONF text

    Args:
        data: Any data that can be converted to JSON
        json_format: JSON formatter to use, default is `json.dumps`

    Returns:
        JONF text, representing this data

    Example::

        text = textwrap.dedent(
            '''\
            compare =
              - true
              = true
            '''
        ).rstrip()

        assert jonf.format({"compare": ["true", True]}) == text
    """
    if _is_unquoted_string(data):
        _, space, text = _format_item(data, is_unquoted_string=True)
        if space == "\n":
            return text

    if data is None or isinstance(data, BASIC_TYPES) or data in EMPTIES:
        return json_format(data)

    if isinstance(data, ARRAYS):
        return "\n".join("".join(_format_item(item)) for item in data)

    if isinstance(data, OBJECTS):
        chunks = []
        for key, value in data.items():
            if not isinstance(key, str):
                raise TypeError(f"Object key should be string, found: {repr(key)}")

            if any(
                mark in key for mark in OBJECT_KEY_MARKS_TO_QUOTE
            ) or not _is_unquoted_string(key):
                key = json_format(key)

            marker, space, value = _format_item(value)
            chunks.append(f"{key} {marker}{space}{value}")
        return "\n".join(chunks)

    # This will probably raise `TypeError: Object of type ... is not JSON serializable`
    # unless custom JSON formatter knows how to serialize it
    return json_format(data)


def _format_item(item: Any, is_unquoted_string: bool = False) -> Tuple[str, str, str]:
    """
    Formats Python nested item to JONF marker, space, text

    Args:
        item: Any data that can be converted to JSON
        is_unquoted_string: If we already found that `_is_unquoted_string(item) is True`

    Returns:
        marker: Either "-" or "="
        space: Either " " or "\n"
        text: JONF text, representing this item
    """
    if is_unquoted_string or _is_unquoted_string(item):
        marker = "-"
        text = item
    else:
        marker = "="
        text = format(item)

    lines = text.splitlines()
    assert lines

    if len(lines) == 1 and (not isinstance(item, COLLECTIONS) or item in EMPTIES):
        space = " "
    else:
        space = "\n"
        text = "\n".join(((INDENT + line) if line else "") for line in lines)

    return marker, space, text


def _is_unquoted_string(data: Any) -> bool:
    """
    Finds if this data should be represented as a JONF unquoted string
    """
    return bool(
        isinstance(data, str)
        and data
        and data.strip() == data
        and not _has_comment(data)
    )


def _has_comment(data: str) -> bool:
    """
    Finds if this string data should be formatted as a quoted JSON string,
    because otherwise a part of this data will become a JONF comment
    """
    return data.startswith("#") or any(mark in data for mark in INNER_COMMENT_MARKS)
    # TODO: Compare performance with regex


# TODO: Full coverage by tests, at the moment only the examples from docs are tested
