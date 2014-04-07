#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
modifying decorators for HTTP method functions

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import json
from seshat.response import Response
import seshat_addons.utils.patch_json
from seshat_addons.view.template import template
import seshat.actions as actions


def HTML(f):
    def wrapper(*args, **kwargs):
        self = args[0]

        data = {
            "title": self._title if self._title else "Untitled",
            "session": self.session,
            "req": self.request
        }
        self.view = template(self._tmpl, data)

        res = f(*args, **kwargs)

        if isinstance(res, actions.BaseAction) or isinstance(res, Response):
            return res

        if type(res) is dict:
            self.view.data = res
            res = self.view

        if isinstance(res, template):
            string = res.render()

        else:
            string = res

        self.headers.append("Content-Type", "text/html")
        return string

    return wrapper


def JSON(f):
    def wrapper(*args, **kwargs):
        self = args[0]

        res = f(*args, **kwargs)

        if isinstance(res, actions.BaseAction) or isinstance(res, Response):
            return res

        if type(res) is not list:
            res = [res]

        self.headers.append("Content-Type", "application/json")
        return json.dumps(res)

    return wrapper


def Guess(f):
    def wrapper(*args, **kwargs):
        self = args[0]

        res = f(*args, **kwargs)

        if isinstance(res, actions.BaseAction) or isinstance(res, Response):
            return res

        if "text/html" in self.request.headers.accept:
            self.head.add_header("Content-Type", "text/html")
            data = {
                "title": self._title if self._title else "Untitled",
                "session": self.session,
                "req": self.request
            }
            data.update(res)
            view = template(self._tmpl, data).render()

            return view

        if "application/json" in self.request.headers.accept:
            self.headers.append("Content-Type", "application/json")

            t_res = type(res)
            if t_res is dict:
                final_res = json.dumps([res])

            elif t_res is list:
                final_res = json.dumps(res)

            return final_res

        else:
            return unicode(res)

    return wrapper
