import flask_admin_subview as subview
from .formatters import model_link_formatter
from .person_view import PersonView


class PersonsSubview(subview.View, PersonView):
    can_set_page_size = False
    can_delete = False
    column_display_actions = False
    list_template = "persons_subview.html"

    column_formatters = {
        'name': model_link_formatter("person", ""),
    }

    def is_sortable(self, name):
        return False
