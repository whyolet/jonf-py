# JONF parser/formatter in Python

NOTE: This is an early alpha version

- JONF format docs: https://jonf.app/
- Formatter is implemented and [tested](https://github.com/whyolet/jonf-py/blob/main/tests/test_format.py)
- Parser is not implemented [yet](https://jonf.app/#roadmap)
- Python example:

```python
# pip install jonf

import jonf, textwrap

text = textwrap.dedent(
    """\
    compare =
      - true
      = true
    """
).rstrip()

data = {
    "compare": [
        "true",
        True,
    ]
}

# TODO:
# assert jonf.parse(text) == data

assert jonf.format(data) == text

print(jonf.format(data))
```

Output:

```
compare =
  - true
  = true
```
