from flask import abort, current_app
from flask_admin.model import BaseModelView
from wtforms import HiddenField


class View(BaseModelView):
    list_template = "admin/subview/list.html"
    # TODO: support inline edits
    column_editable_list = []
    can_edit = False
    can_view_details = False

    def render(self, template, **kwargs):
        if template != self.list_template:
            current_app.logger.error(u"Not implemented for {}, {}".format(template, kwargs))
            abort(400)
        return super(View, self).render(template, **kwargs)

    def get_action_form(self):
        class ActionForm(super(View, self).get_action_form()):
            id = HiddenField()

        return ActionForm
