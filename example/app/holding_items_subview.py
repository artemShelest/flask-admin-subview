from flask import flash
from flask_admin import expose
from flask_admin.actions import action
from flask_admin.model.template import TemplateLinkRowAction
from sqlalchemy import and_

from .db import Item, db
from .items_subview import ItemsSubview


class HoldingItemsSubview(ItemsSubview):
    can_delete = False
    column_list = ("title", "owner",)

    @action("return", "Return Item", "Confirm return of selected items to owner.")
    def action_return(self, ids):
        Item.query.filter(and_(Item.id.in_(ids))).update({Item.holder_id: Item.owner_id}, synchronize_session=False)
        db.session.commit()
        len_ids = len(ids)
        if len_ids > 1:
            flash("Returned {} items".format(len_ids))
        else:
            flash("Returned an item")

    @expose("/return/", methods=("POST",))
    def return_view(self):
        return self._action_view_base(self.action_return, "Failed to return items. %(error)s")

    def get_list_row_actions(self):
        actions = super(HoldingItemsSubview, self).get_list_row_actions()
        actions.append(TemplateLinkRowAction("item_actions.return_item", "Return item to owner"))
        return actions

    def _apply_query_filter(self, query, client_id):
        return query.filter(Item.holder_id == client_id)
