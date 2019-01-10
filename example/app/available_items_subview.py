from flask import flash, request
from flask_admin import expose
from flask_admin.actions import action
from flask_admin.model.template import TemplateLinkRowAction
from sqlalchemy import and_
from wtforms import HiddenField

from .db import Item, db
from .items_subview import ItemsSubview


class AvailableItemsSubview(ItemsSubview):
    can_delete = False
    column_list = ("title", "owner",)

    @action("borrow", "Borrow Item")
    def action_borrow(self, ids):
        client_id = request.form.get('client_id')
        if not client_id:
            flash("Client id required", "error")
            return
        Item.query.filter(and_(Item.id.in_(ids))).update({Item.holder_id: client_id}, synchronize_session=False)
        db.session.commit()
        len_ids = len(ids)
        if len_ids > 1:
            flash("Borrowed {} items".format(len_ids))
        else:
            flash("Borrowed an item")

    @expose("/borrow/", methods=("POST",))
    def borrow_view(self):
        return self._action_view_base(self.action_borrow, "Failed to borrow items. %(error)s")

    def get_list_row_actions(self):
        actions = super(AvailableItemsSubview, self).get_list_row_actions()
        actions.append(TemplateLinkRowAction("item_actions.borrow_item", "Borrow item"))
        return actions

    def _apply_query_filter(self, query, client_id):
        return query.filter(and_(Item.holder_id != client_id, Item.holder_id == Item.owner_id))

    def get_action_form(self):
        class ActionForm(super(AvailableItemsSubview, self).get_action_form()):
            client_id = HiddenField()

        return ActionForm

    def action_form(self, obj=None):
        f = super(AvailableItemsSubview, self).action_form(obj)
        f.client_id.data = request.args.get('id')
        return f
