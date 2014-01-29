#!/usr/bin/env python
"""
TEMPLATE ALL THE THINGS WITH Jinja (And Mustache)!!!!
Uses the Jinja templating language to make a base template object by which is
easy to work with in the controllers, and a walker and templateFile objects
which provide automatic reading and rereading in debug mode of template files.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import pystache
import os
import logging
import yaml
import jinja2
import arrow
import copy
import re

logger = logging.getLogger("seshat.views")


dynamic_reloading = False
templates_base = "views/"
time_format = "dd MMM DD HH:mm:ss:SS YYYY"
config_delim = "+++"
default_theme_color = "green"
partial_syntax_regex = r'(\!\[{2}(?:.*?)\]{2})'


tmpls = {}
partial_re = re.compile(partial_syntax_regex)
partials_ready = False


class templateFile(object):
    def __init__(self, fileBit):
        """
        Reads in fileBit into memory, and sets the modified time for the
        object to that of the file at the current moment.
        """
        self._file_bit = fileBit
        self._file = ''.join([templates_base, fileBit])
        self._mtime = 0

        self._config = {}
        self._read_template()

    def _read_template(self):
        """
        Read in the template only if it has been modified since we first
        read it into our `_template`
        """
        mtime = os.path.getmtime(self._file)

        nt = arrow.get(mtime).format(time_format)
        logger.debug("""\n\r============== Template =================
    Reading template into memory...
    TEMPLATE:  %s
    TYPE: %s
    MTIME: %s
""" % (self._file, self.extension, nt))

        with open(self._file, "r") as openTmpl:
            raw = unicode(openTmpl.read())

        self._mtime = mtime
        self._parse_raw(raw)

    def _parse_raw(self, raw):
        if raw[:3] == config_delim:
            config, template = raw.split(config_delim, 2)[1:]
            self._config = yaml.load(config)
        else:
            self._config = {}
            template = raw

        self._raw_template = template

    def _raw_to_engine(self, raw):
        if(self.is_mustache):
            self._engine_template = raw

        if(self.is_jinja):
            self._engine_template = jinja2.Template(raw)

    def _parse_partials(self):
        updated = False
        partials = []
        matches = partial_re.findall(self._raw_template)

        if matches:
            for match in matches:
                name = match[:len(match)-2][3:]
                partials.append(match)
                updated = updated or tmpls[name]._update_template()

        return updated, partials

    def _replace_partials(self, partials):
        pre_engine = copy.copy(self._raw_template)
        try:
            for match in partials:
                logger.debug("""============= Partial =============
    REPLACING: {}
    PARENT TEMPLATE:{}""".format(match, self._file))
                name = match[:len(match)-2][3:]
                pattern = "({})".format(re.escape(match))
                pattern_regex = re.compile(pattern)
                pre_engine = re.sub(pattern_regex, tmpls[name].template, pre_engine)

            self._raw_to_engine(pre_engine)

        except KeyError:
            raise KeyError("Couldn't find the template {}, as a partial of {}".format(name, self._file_bit))

    def _update_template(self):
        updated = False
        mtime = os.path.getmtime(self._file)

        if self._mtime < mtime:
            pt = arrow.get(self._mtime).format(time_format)
            nt = arrow.get(mtime).format(time_format)
            logger.debug("""\n\r============== Template =================
    Updating template...
    TEMPLATE:  %s
    TYPE: %s
    OLD MTIME: %s
    NEW MTIME: %s
""" % (self._file, self.extension, pt, nt))

            self._read_template()
            updated = True

        update, partials = self._parse_partials()
        if update or updated:
            self._replace_partials(partials)
            updated = True

        return updated

    @property
    def template(self):
        if dynamic_reloading:
            self._update_template()

        return self._raw_template

    @property
    def config(self):
        return self._config

    @property
    def extension(self):
        return self._file.rsplit(".", 1)[1]

    @property
    def is_jinja(self):
        return self.extension=="jinja"

    @property
    def is_mustache(self):
        return self.extension=="mustache"

    def render(self, data):
        if dynamic_reloading:
            self._update_template()

        _data = copy.deepcopy(self._config)
        _data.update(data)

        if(self.is_jinja):
            wat = unicode(self._engine_template.render(_data))
        else:
            result = pystache.render(self._engine_template, _data)
            wat = unicode(result)

        del _data
        return wat

    def __contains__(self, item):
        return item in self._config

    def __getitem__(self, item):
        return self._config[item]

    def __setitem__(self, item, value):
        self._config[item] = value


class template(object):
    def __init__(self, template, request=None, additional_data=None):
        self._baseData = {
            "title": "",
            "stylesheets": [],
            "scripts": "",
            "scriptFiles": [],
            "breadcrumbs": False,
            "breadcrumbs_top": False,
        }
        if additional_data:
            self._baseData.update(additional_data)
        if request:
            self._baseData["req"] = request

        self._template = template
        self._base = "skeletons/navbar"

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        assert type(value) is str
        self._template = value

    @property
    def skeleton(self):
        return self._base

    @skeleton.setter
    def skeleton(self, value):
        assert type(value) == str
        self._base = value

    @skeleton.deleter
    def skeleton(self):
        self._base = ""

    @property
    def data(self):
        return self._baseData

    @data.setter
    def data(self, value):
        assert type(value) == dict
        self._baseData.update(value)

    @property
    def title(self):
        return self._baseData["title"]

    @title.setter
    def title(self, value):
        self._baseData.update({"title": value})

    def append(self, value):
        self.data = value

    def update(self, value):
        self.data = value

    @property
    def scripts(self):
        return self._baseData["scriptFiles"], self._baseData["scripts"]

    @scripts.setter
    def scripts(self, value):
        if type(value) == list:
            self._baseData["scriptFiles"].extend(value)
        else:
          self._baseData["scripts"] += value

    @property
    def stylesheets(self):
        return self._baseData["stylesheets"], self._baseData["styles"]

    @stylesheets.setter
    def stylesheets(self, value):
        if type(value) == list:
            self._baseData["stylesheets"].extend(value)
        else:
            self._baseData["styles"] += value

    @stylesheets.deleter
    def stylesheets(self):
        self._baseData["stylesheets"] = []

    def partial(self, placeholder, template, data=None):
        try:
            if data is None: data = {}
            assert type(data) is dict
            data.update(self._baseData.copy())
            self._baseData[placeholder] = tmpls[template].render(data)
        except KeyError:
            raise KeyError("Couldn't find the template {} when used as a partial".format(template))

    def render(self):
        data = self._baseData.copy()

        template = tmpls[self._template]
        body = template.render(data)

        data.update(template.config)

        if "base" in template:
            base = template["base"]
        else:
            base = self._base

        if not "theme_color" in template and not "theme_color" in data:
            data["theme_color"] = default_theme_color

        if base is not None and base:
            baseTmpl= tmpls[base]
            data["body"] = body

            _render = baseTmpl.render(data)

        else:
            _render = body

        del data
        del self._baseData

        return unicode(_render)


class PartialTemplate(template):
    def render(self):
        data = self._baseData.copy()

        template = tmpls[self._template]
        body = template.render(data)

        body = body if body else ""

        del data

        return unicode(body)


def read_in_templates():
    global partials_ready
    global tmpls
  # Parse all template files into a template object
    for top, folders, files in os.walk(templates_base):
        for fi in files:
            base = top.split(templates_base)[1]
            file_name, extension = fi.rsplit('.', 1)
            if extension in ["mustache", "jinja"]:
                name = '/'.join([base, file_name]).lstrip('/')
                fi = '/'.join([base, fi])
                tmpls[name] = templateFile(fi)

    partials_ready = True

    logger.debug("Parsing templates for partials and performing replacements.")
  # Parse all partials within the templates, replacing the partial text with the
  # given partial, so that we have support for partials in both mustache and
  # jinja with the same syntax (which is currently ![[name/of/partial]])
    for key, tmpl in tmpls.iteritems():
        updated, partials = tmpl._parse_partials()
        tmpl._replace_partials(partials)
