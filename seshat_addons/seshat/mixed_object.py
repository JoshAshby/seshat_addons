#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
baseObject to build pages off of

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.controller import Controller
from collections import namedtuple
from seshat.actions import Redirect, Unauthorized
root_group = "root"


def check_groups(groups, user_groups):
    return len(set(groups).intersection(set(user_groups))) >= 1


class MixedObject(Controller):
    _login = namedtuple('Login', ['login', 'quiet'])(False, False)
    _no_login = False
    _groups = None
    _redirect_url = ""
    _tmpl = None
    _title = None

    def pre_content_hook(self):
        if self._no_login and self.session.id:
            self.session.push_alert("That page is only for non logged in people. Weird huh?", level="info")
            if not self._redirect_url:
                return Redirect("/")
            else:
                return Redirect(self._redirect_url)

        if self._login.login and not self.session.id:
            if not self._login.quiet:
                self.session.push_alert("You need to be logged in to view this page.", level="error")

            if not self._redirect_url:
                return Unauthorized()
            else:
                return Redirect(self._redirect_url)

        if self._groups:
            if not check_groups(self._groups, self.session.groups):
                if not self.session.has_perm(root_group):
                    self.session.push_alert("You are not authorized to perfom this action.", level="error")
                    if not self._redirect_url:
                        return Unauthorized()
                    else:
                        return Redirect(self._redirect_url)

        return None
