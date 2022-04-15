# JONF parser/formatter in Python

NOTE: This is initial stub version, docs and tests only

- JONF format: https://jonf.app/

- Python example:

```python
# pip install jonf

import jonf

text = """\
compare =
  - true
  = true
"""

assert jonf.parse(text) == {"compare": ["true", True]}

assert jonf.format({"compare": ["true", True]}) == text
```

- TODO: Implement `jonf.parse()` and `jonf.format()` as part of [JONF Roadmap](https://jonf.app/#roadmap)
