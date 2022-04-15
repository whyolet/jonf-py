import pytest

import jonf


def test_format() -> None:
    with pytest.raises(NotImplementedError):
        jonf.format({"compare": ["true", True]})

    # TODO:
    #
    # text = """\
    # compare =
    #   - true
    #   = true
    # """
    #
    # assert jonf.format({"compare": ["true", True]}) == text
