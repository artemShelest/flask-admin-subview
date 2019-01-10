from flask_admin.contrib.sqla import ModelView

from flask_admin_subview import SubviewContainerMixin, SubviewEntry


class PersonView(SubviewContainerMixin, ModelView):
    can_view_details = True
    can_set_page_size = True
    column_searchable_list = ("name",)
    column_sortable_list = ("name", "num_own", "num_holding", "num_borrowed")
    column_editable_list = ("name",)

    column_filters = ("name",)
    column_list = ("name", "num_own", "num_holding", "num_borrowed")
    column_details_list = ("name",)

    form_create_rules = ("name",)
    form_edit_rules = form_create_rules

    subviews = (
        SubviewEntry("/holding_items/", "Holding Items", "id"),
        SubviewEntry("/own_items/", "Own Items", "id"),
        SubviewEntry("/available_items/", "Available Items", "id"),
    )

    _extra_js = ("/static/reloader.js",)
