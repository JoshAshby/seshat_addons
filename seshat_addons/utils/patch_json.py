#!/usr/bin/env python
"""Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "__json__()"
method and uses it to encode the object if found.

Stolen from the wonderful answer by martineau here:
    http://stackoverflow.com/a/18561055
"""
import json

def _default(self, obj):
    return getattr(obj.__class__, "__json__", _default.default)(obj)

_default.default = json.JSONEncoder().default # save unmodified default
json.JSONEncoder.default = _default # replacement
