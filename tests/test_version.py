import jonf


def test_jonf_package_version() -> None:
    assert jonf.__version__ == "0.0.6"

    with open("pyproject.toml", "r") as pyproject:
        assert pyproject.readlines()[2] == f'version = "{jonf.__version__}"\n'


def test_jonf_format_version() -> None:
    assert jonf.__jonf_format_version__ == "0.0.13"
