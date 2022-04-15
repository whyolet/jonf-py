import textwrap

import pytest

import jonf


def test_parse() -> None:
    text = textwrap.dedent(
        """\
        compare =
          - true
          = true
        """
    ).rstrip()

    with pytest.raises(NotImplementedError):
        jonf.parse(text)

    # TODO:
    #
    # assert jonf.parse(text) == {"compare": ["true", True]}
