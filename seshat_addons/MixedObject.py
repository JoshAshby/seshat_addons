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
import seshat.base_object as base
from seshat.head import Head

root_group = "root"


def check_groups(groups, user_groups):
    return len(set(groups).intersection(set(user_groups))) >= 1


class MixedObject(base.BaseObject):
    _login = (False, False)
    _no_login = False
    _groups = None
    _redirect_url = ""
    _tmpl = None
    _title = None

    def post_init_hook(self):
        self.head = Head("200 OK")

    def _build(self):
        if self._no_login and self.request.session.id:
            self.request.session.push_alert("That page is only for non logged in people. Weird huh?", level="info")
            if not self._redirect_url:
                self.head = Head("303 SEE OTHER", [("Location", "/")])
            else:
                self.head = Head("303 SEE OTHER", [("Location", self._redirect_url)])
            return "", self.head

        if self._login[0] and not self.request.session.id:
            if not self._login[1]:
                self.request.session.push_alert("You need to be logged in to view this page.", level="error")

            if not self._redirect_url:
                self.head = Head("401 UNAUTHORIZED")
            else:
                self.head = Head("303 SEE OTHER", [("Location", self._redirect_url)])
            return "", self.head

        if self._groups:
            if not check_groups(self._groups, self.request.session.groups):
                if not self.request.session.has_perm(root_group):
                    self.request.session.push_alert("You are not authorized to perfom this action.", level="error")
                    if not self._redirect_url:
                        self.head = Head("401 UNAUTHORIZED")
                    else:
                        self.head = Head("303 SEE OTHER", [("Location", self._redirect_url)])
                    return "", self.head

        content, self.head = super(MixedObject, self)._build()

        if self.head.status not in ["303 SEE OTHER"]:
            del self.request.session.alerts

        return content, self.head
