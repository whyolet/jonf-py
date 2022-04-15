import pytest

import jonf


def test_parse() -> None:
    text = """\
compare =
  - true
  = true
"""

    with pytest.raises(NotImplementedError):
        jonf.parse(text)

    # TODO:
    #
    # assert jonf.parse(text) == {"compare": ["true", True]}
