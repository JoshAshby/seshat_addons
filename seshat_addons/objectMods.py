#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
modifying decorators for classes

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""


def login(groups=None, redirect="", quiet=False):
    if groups is None:
        groups = []
    def wrapper(HTTPObject):
        HTTPObject._login = (True, quiet)
        HTTPObject._groups = groups
        HTTPObject._redirect_url = redirect
        return HTTPObject
    return wrapper


def not_logged_in(redirect=""):
    def wrapper(HTTPObject):
        HTTPObject._login = (False, False)
        HTTPObject._no_login = True
        HTTPObject._redirect_url = redirect
        return HTTPObject
    return wrapper


def template(template, title=None):
    def wrapper(HTTPObject):
        HTTPObject._title = title
        HTTPObject._tmpl = template

        return HTTPObject
    return wrapper
