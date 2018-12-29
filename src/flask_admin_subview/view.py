from flask import abort, current_app
from flask_admin import BaseView


class View(BaseView):
    list_template = "admin/subview/list.html"
    column_editable_list = []
    can_edit = False
    can_view_details = False

    def render(self, template, **kwargs):
        if template != self.list_template:
            current_app.logger.error(u"Not implemented for {}, {}".format(template, kwargs))
            abort(400)
        return super(View, self).render(template, **kwargs)
