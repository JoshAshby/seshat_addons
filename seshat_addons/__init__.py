#!/usr/bin/env python
__version__ = '0.1.0'
VERSION = tuple(map(int, __version__.split('.')))

import .seshat
import .view

__all__ = [
    "seshat.func_mods",
    "seshat.mixed_object",
    "seshat.obj_mods",
    "seshat.request_item",
    "view.template"
    ]
