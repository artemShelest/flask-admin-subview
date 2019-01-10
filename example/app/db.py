from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, func, and_
from sqlalchemy.orm import column_property

db = SQLAlchemy()


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255), nullable=False, unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("person.id", ondelete="CASCADE"), nullable=False)
    holder_id = db.Column(db.Integer, db.ForeignKey("person.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return self.title


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255), nullable=False, unique=True)
    own_items = db.relationship("Item", cascade="all,delete", foreign_keys=Item.owner_id, backref="owner", lazy=True)
    holding_items = db.relationship("Item", cascade="all,delete", foreign_keys=Item.holder_id, backref="holder",
                                    lazy=True)

    num_own = column_property(select([func.count(Item.id)]).where(id == Item.owner_id).correlate_except(Item))
    num_holding = column_property(select([func.count(Item.id)]).where(id == Item.holder_id).correlate_except(Item))
    num_borrowed = column_property(select([func.count(Item.id)]).where(
        and_(id == Item.holder_id, Item.owner_id != Item.holder_id)).correlate_except(Item))

    def __repr__(self):
        return self.name
