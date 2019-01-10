from flask_admin.contrib.sqla import ModelView

from .formatters import model_link_formatter


class ItemView(ModelView):
    details_modal = True
    can_view_details = True
    can_set_page_size = True
    column_searchable_list = ("title",)
    column_sortable_list = ("title", ("owner", "owner.name"), ("holder", "holder.name"))
    column_filters = ("title",)
    column_list = ("title", "owner", "holder")
    column_editable_list = ("title",)
    form_create_rules = ("title", "owner", "holder")
    form_edit_rules = ("title",)

    column_formatters = {
        'owner': model_link_formatter("person", "owner"),
        'holder': model_link_formatter("person", "holder")
    }
