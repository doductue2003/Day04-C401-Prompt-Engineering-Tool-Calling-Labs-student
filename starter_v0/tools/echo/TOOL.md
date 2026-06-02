---
name: echo
summary: "Return the input text unchanged — useful for testing routing and arguments."
---

## Purpose

The `echo` tool returns the provided `text` argument verbatim in a JSON-like result.
It is intended for tests where the agent should route to a simple, side-effect-free tool.

## Parameters

- `text` (string, required): the text to echo back.

## Example

```py
from tools import TOOL_FUNCTIONS as T
T['echo']('hello')['echoed']  # => 'hello'
```
