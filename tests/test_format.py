import textwrap

import jonf


def test_format_from_jonf_py_example() -> None:
    text = textwrap.dedent(
        """\
        compare =
          - true
          = true
        """
    ).rstrip()

    assert jonf.format({"compare": ["true", True]}) == text


def test_format_from_jonf_app_quick_example() -> None:
    text = textwrap.dedent(
        """\
        name - Deep Thought
        answer - 42
        hardware =
          cores = 42
          eyes =
            left - green
            right - violet
        about -
          indented, unquoted,
          and raw - \\no special chars

          multiline string here
        pets =
          - cat
          - dog
          - turtle
        friends =
          =
            name - Alice
            age = null
          =
            name - Bob
            age = 42
        scripts =
          check -
            set -eu
            DIRS="src tests"
            lint $DIRS
            test $DIRS
        """
    ).rstrip()

    data = {
        "name": "Deep Thought",
        "answer": "42",
        "hardware": {"cores": 42, "eyes": {"left": "green", "right": "violet"}},
        "about": "indented, unquoted,\nand raw - \\no special chars\n\n"
        "multiline string here",
        "pets": ["cat", "dog", "turtle"],
        "friends": [{"name": "Alice", "age": None}, {"name": "Bob", "age": 42}],
        "scripts": {"check": 'set -eu\nDIRS="src tests"\nlint $DIRS\ntest $DIRS'},
    }

    assert jonf.format(data) == text


def test_format_1_simple_root_values() -> None:
    assert jonf.format("some string") == '"some string"'
    assert jonf.format(-3.14) == "-3.14"
    assert jonf.format(True) == "true"
    assert jonf.format(False) == "false"
    assert jonf.format(None) == "null"


def test_format_1_indented_unquoted_multiline_string() -> None:
    text = """\
  indented unquoted
  multiline

  string"""

    assert jonf.format("indented unquoted\nmultiline\n\nstring") == text


def test_format_2_jonf_array() -> None:
    text = textwrap.dedent(
        r"""        - Alice in Wonderland
        -
          multiline
          string

          here
        = "  explici\t whitespace \n"
        - unquoted is raw - \no special chars"
        - great for regex: [\n\r\t]+
        - 42
        = 42
        - -3.14
        = -3.14
        - true
        = true
        - false
        = false
        - null
        = null
        - []
        = []
        - {}
        = {}
        """
    ).rstrip()

    data = [
        "Alice in Wonderland",
        "multiline\nstring\n\nhere",
        # "multiline\nstring\n\nhere",  # Formatter makes unquoted string from it again
        "  explici\t whitespace \n",
        'unquoted is raw - \\no special chars"',
        "great for regex: [\\n\\r\\t]+",
        "42",
        42,
        "-3.14",
        -3.14,
        "true",
        True,
        "false",
        False,
        "null",
        None,
        "[]",
        [],
        "{}",
        {},
    ]

    assert jonf.format(data) == text


def test_format_3_jonf_object() -> None:
    text = textwrap.dedent(
        """\
        name - Deep Thought
        answer - 42
        cores = 42
        "some - strange = key" - value
        42 - keys are always strings
        true - even with =, it affects values only
        """
        # The last line is `true = "even with =, it affects values only"` in the docs
        # to show parser behavior, while formatter makes correct unquoted string here
    ).rstrip()

    data = {
        "name": "Deep Thought",
        "answer": "42",
        "cores": 42,
        "some - strange = key": "value",
        "42": "keys are always strings",
        "true": "even with =, it affects values only",
    }

    assert jonf.format(data) == text


def test_format_4_object_in_object() -> None:
    text = textwrap.dedent(
        """\
        type - dragon
        eyes =
          left - green
          right - violet
        """
    ).rstrip()

    data = {"type": "dragon", "eyes": {"left": "green", "right": "violet"}}

    assert jonf.format(data) == text


def test_format_5_object_in_array() -> None:
    text = textwrap.dedent(
        """\
        =
          name - Alice
          age = null
        =
          name - Bob
          age = 42
        """
    ).rstrip()

    data = [{"name": "Alice", "age": None}, {"name": "Bob", "age": 42}]

    assert jonf.format(data) == text


def test_format_5_object_in_array_with_unquoted_string_marker() -> None:
    text = textwrap.dedent(
        """\
        - unquoted string
        -
          multiline - unquoted
          string = here
        """
    ).rstrip()

    data = ["unquoted string", "multiline - unquoted\nstring = here"]

    assert jonf.format(data) == text


def test_format_7_array_in_object() -> None:
    text = textwrap.dedent(
        """\
        name - Bob
        kids =
          - Charlie
          - Dave
          - Eve
        """
    ).rstrip()

    data = {"name": "Bob", "kids": ["Charlie", "Dave", "Eve"]}

    assert jonf.format(data) == text


def test_format_8_array_in_array() -> None:
    text = textwrap.dedent(
        """\
        =
          - We
          - are
        =
          - almost
          =
            - done!
        """
    ).rstrip()

    data = [["We", "are"], ["almost", ["done!"]]]

    assert jonf.format(data) == text


def test_format_9_comment() -> None:
    text = textwrap.dedent(
        """\
        name - Alice
        url - https://example.org/#alice
        location = "Wonderland # 42"
        """
        # Of course formatter can not add comments as they are not part of the data
    ).rstrip()

    data = {
        "name": "Alice",
        "url": "https://example.org/#alice",
        "location": "Wonderland # 42",
    }

    assert jonf.format(data) == text


def test_format_10_dsl() -> None:
    text = textwrap.dedent(
        """\
        custom =
          debug = true
          verbose - ${self:custom.debug}
        """
    ).rstrip()

    data = {"custom": {"debug": True, "verbose": "${self:custom.debug}"}}

    # Parsed by DSL, not here:
    # data = {"custom": {"debug": True, "verbose": True}}

    assert jonf.format(data) == text
