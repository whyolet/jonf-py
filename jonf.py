"""JONF parser/formatter in Python - https://jonf.app/"""

__version__ = "0.0.3"
__jonf_format_version__ = "0.0.11"

import json
from typing import Any, Callable


def parse(text: str, json_parse: Callable[[str], Any] = json.loads) -> Any:
    """Parses JONF text to Python data

    Args:
        text: JONF text
        json_parse: JSON parser to use, default is `json.loads`

    Returns:
        Python data, parsed from this text

    Example::

        import jonf
        from textwrap import dedent

        assert jonf.parse(dedent('''\
          compare =
            - true
            = true
        ''')) == {"compare": ["true", True]}
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

        import jonf
        from textwrap import dedent

        assert jonf.format({"compare": ["true", True]}) == dedent('''\
          compare =
            - true
            = true
        ''')
    """
    raise NotImplementedError
