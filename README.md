# bioio-sldy

[![Build Status](https://github.com/bioio-devs/bioio-sldy/workflows/CI/badge.svg)](https://github.com/bioio-devs/bioio-sldy/actions)
[![Documentation](https://github.com/bioio-devs/bioio-sldy/workflows/Documentation/badge.svg)](https://bioio-devs.github.io/bioio-sldy)

A BioIO reader plugin for reading 3i slidebook (SLDY) images.

This plugin is intended to be used in conjunction with [bioio](https://github.com/bioio-devs/bioio)

---

## Installation

**Stable Release:** `pip install bioio-sldy`<br>
**Development Head:** `pip install git+https://github.com/bioio-devs/bioio-sldy.git`

## Quickstart

```python
from bioio_sldy import Reader 

r = Reader("my-image.ext")
r.dims
```

## Documentation

For full package documentation please visit [bioio-devs.github.io/bioio-sldy](https://bioio-devs.github.io/bioio-sldy).

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

**MIT License**
