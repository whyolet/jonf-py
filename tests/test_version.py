import jonf


def test_jonf_package_version() -> None:
    assert jonf.__version__ == "0.0.2"


def test_jonf_format_version() -> None:
    assert jonf.__jonf_format_version__ == "0.0.11"
