from collections import namedtuple

from flask import current_app

from .subview import Subview


class SubviewEntry(namedtuple("SubviewEntry", "endpoint, title, injectParam, attr")):
    @property
    def attr_formatted(self):
        if not self.attr:
            return ""
        return u" ".join(u'{}="{}"'.format(k, v) for k, v in self.attr.items())


SubviewEntry.__new__.__defaults__ = (None,) * len(SubviewEntry._fields)


class SubviewContainerMixin(object):
    details_template = "admin/model/details_with_subview.html"
    subview_ext_name = Subview.EXT_NAME
    subviews = []
    _extra_js = []

    @property
    def extra_js(self):
        return [current_app.extensions[self.subview_ext_name].js_url()] + list(self._extra_js)
