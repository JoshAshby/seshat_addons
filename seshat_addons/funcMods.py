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
from views.template import template
import seshat.actions as actions


def HTML(f):
    def wrapper(*args, **kwargs):
        self = args[0]

        data = {"title": self._title if self._title else "Untitled"}
        self.view = template(self._tmpl, self.request, data)

        res = f(*args, **kwargs)

        self.head.add_header("Content-Type", "text/html")

        if isinstance(res, template):
            string = res.render()
        else:
            string = res

        del res
        return string

    return wrapper


def JSON(f):
    def wrapper(*args, **kwargs):
        self = args[0]
        res = f(*args, **kwargs)
        if isinstance(res, actions.Unauthorized) or isinstance(res, actions.NotFound):
            return [{"error": res.head[0]}]

        if type(res) is dict:
            self.head.add_header("Content-Type", "application/json")
            return json.dumps([res])

        elif type(res) is list:
            self.head.add_header("Content-Type", "application/json")
            return json.dumps(res)

        else:
            return res

    return wrapper


def Guess(f):
    def wrapper(*args, **kwargs):
        self = args[0]

        data = {"title": self._title if self._title else "Untitled"}
        self.view = template(self._tmpl, self.request, data)

        res = f(*args, **kwargs)
        t_res = type(res)

        if isinstance(res, actions.BaseAction):
            return res

        if isinstance(res, template):
            final_res = res.render()

        elif t_res is str:
            final_res = res

        elif t_res is dict:
            final_res = json.dumps([res])

        elif t_res is list:
            final_res = json.dumps(res)

        del res

        if self.request.accepts("html") or self.request.accepts("*/*"):
            self.head.add_header("Content-Type", "text/html")
            return final_res

        elif self.request.accepts("json") or self.request.accepts("*/*"):
            self.head.add_header("Content-Type", "application/json")
            return json.dumps([final_res])

    return wrapper
