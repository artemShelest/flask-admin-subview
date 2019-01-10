from flask import url_for
from markupsafe import Markup


def model_link_formatter(section, attr, view_type="details_view"):
    def wrapped(view, context, model, name):
        obj = getattr(model, attr) if attr else model
        return Markup(
            u"<a href='{}'>{}</a>".format(url_for("{}.{}".format(section, view_type), id=obj.id), obj)) if obj else u""

    return wrapped
