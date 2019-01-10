from flask import Flask
from flask_admin import Admin, AdminIndexView

from .available_items_subview import AvailableItemsSubview
from .holding_items_subview import HoldingItemsSubview
from .items_subview import ItemsSubview
from .persons_subview import PersonsSubview
from .person_view import PersonView
from .item_view import ItemView
from .db import Person, Item, db
from flask_admin_subview import Subview

app = Flask(__name__)

app.config['SECRET_KEY'] = '123456790'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

admin = Admin(app, name="Flask-Admin Subview Example", base_template='layout.html', template_mode="bootstrap3",
              index_view=AdminIndexView(template='index.html', url='/'))
admin.add_view(PersonView(model=Person, session=db.session, endpoint="person"))
admin.add_view(ItemView(model=Item, session=db.session, endpoint="item"))
app.register_blueprint(
    PersonsSubview(Person, db.session, "Persons", endpoint="persons_subview").create_blueprint(admin))
app.register_blueprint(ItemsSubview(Item, db.session, "Own Items", endpoint="own_items").create_blueprint(admin))
app.register_blueprint(
    HoldingItemsSubview(Item, db.session, "Holding Items", endpoint="holding_items").create_blueprint(admin))
app.register_blueprint(
    AvailableItemsSubview(Item, db.session, "Available Items", endpoint="available_items").create_blueprint(admin))
Subview(app)
