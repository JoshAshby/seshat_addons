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
import seshat_addons.utils.patch_json
from ..view.template import template
import seshat.actions as actions


def HTML(f):
    def wrapper(*args, **kwargs):
        self = args[0]

        data = {"title": self._title if self._title else "Untitled"}
        self.view = template(self._tmpl, self.request, data)

        res = f(*args, **kwargs)

        if isinstance(res, actions.BaseAction):
            return res

        if type(res) is dict:
            self.view.data = res
            res = self.view

        if isinstance(res, template):
            string = res.render()

        else:
            string = res

        del res

        self.head.add_header("Content-Type", "text/html")
        return string

    return wrapper


def JSON(f):
    def wrapper(*args, **kwargs):
        self = args[0]

        res = f(*args, **kwargs)

        if isinstance(res, actions.BaseAction):
            return res

        if type(res) is dict:
            res = [res]

        self.head.add_header("Content-Type", "application/json")
        return json.dumps(res)

    return wrapper


def Guess(f):
    def wrapper(*args, **kwargs):
        self = args[0]

        res = f(*args, **kwargs)

        if isinstance(res, actions.BaseAction):
            return res

        if self.request.accepts("html") or self.request.accepts("*/*"):
            self.head.add_header("Content-Type", "text/html")
            data = {"title": self._title if self._title else "Untitled"}
            data.update(res)
            view = template(self._tmpl, self.request, data).render()

            del res

            return view

        if self.request.accepts("json") or self.request.accepts("*/*"):
            self.head.add_header("Content-Type", "application/json")

            t_res = type(res)
            if t_res is dict:
                final_res = json.dumps([res])

            elif t_res is list:
                final_res = json.dumps(res)

            del res

            return final_res

        else:
            return unicode(res)

    return wrapper
