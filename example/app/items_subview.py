from flask import request, abort, redirect
from flask_admin.helpers import get_redirect_target, flash_errors

import flask_admin_subview as subview
from .db import Item
from .formatters import model_link_formatter
from .item_view import ItemView


class ItemsSubview(subview.View, ItemView):
    can_delete = True
    list_template = "items_subview.html"
    column_list = ("title", "holder",)

    def get_query(self):
        return self._extend_query(super(ItemsSubview, self).get_query())

    def get_count_query(self):
        return self._extend_query(super(ItemsSubview, self).get_count_query())

    def _apply_query_filter(self, query, client_id):
        return query.filter(Item.owner_id == client_id)

    def _extend_query(self, query):
        client_id = request.args.get('id')
        if client_id is None:
            abort(400, "Client id required")
        return self._apply_query_filter(query, client_id)

    column_formatters = {
        'title': model_link_formatter("item", ""),
    }

    def _action_view_base(self, action, error_msg):
        return_url = get_redirect_target() or self.get_url(".index_view")
        form = self.action_form()
        if self.validate_form(form):
            action((request.form.get('id'),))
            return redirect(return_url)
        else:
            flash_errors(form, message=error_msg)
        return redirect(return_url)


ItemsSubview.column_formatters.update(ItemView.column_formatters)
