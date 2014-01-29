#!/usr/bin/env python
__version__ = '0.1.0'
VERSION = tuple(map(int, __version__.split('.')))

import view
import addons

__all__ = [
    "addons",
    "view"
    ]
