"""JONF parser/formatter in Python - https://jonf.app/"""

__version__ = "0.0.1"
__jonf_format_version__ = "0.0.11"

from typing import Any


def parse(text: str) -> Any:
    """Parses JONF text to Python data

    Args:
        text: JONF text

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


def format(data: Any) -> str:
    """Formats Python data to JONF text

    Args:
        data: Any data that can be converted to JSON

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
