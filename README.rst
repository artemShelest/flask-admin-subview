Flask-Admin-Subview
===================

Embed Flask-Admin list views to an arbitrary page:

.. image:: https://raw.githubusercontent.com/artemShelest/flask-admin-subview/master/res/screen1.png

.. image:: https://raw.githubusercontent.com/artemShelest/flask-admin-subview/master/res/screen2.png

Limitations
===========

- Inline edits are not supported
- Bootstrap3 templates only

Installation
============

.. code-block:: console

    pip install flask-admin-subview


Integration
===========

The easiest way to integrate is to use helpers for the details view of the model. The following example demonstrates
integration of subview to show relations of SQLAlchemy model in the details page.

**DB Schema**

.. code-block:: python

    class ContentModel(db.Model):
        __table__ = "content"
        id = db.Column(db.Integer, primary_key=True)
        container_id = db.Column(db.Integer, db.ForeignKey("container.id"), nullable=False)

    class ContainerModel(db.Model):
        __table__ = "container"
        id = db.Column(db.Integer, primary_key=True)
        content = db.relationship(ContentModel)


**Prepare your subview**

It is a good idea to subclass existing view of your model:

.. code-block:: python

    import flask_admin_subview

    class ContentModelSubview(flask_admin_subview.View, ContentModelView):
        pass


Or you can create a brand-new view for the subview:

.. code-block:: python

    from flask_admin.contrib.sqla import ModelView
    import flask_admin_subview

    class ContentModelSubview(flask_admin_subview.View, ModelView):
        pass


Add query filter to show content for certain container only, container id will be passed as a URL parameter:

.. code-block:: python

    class ContentModelSubview(...):
        def get_query(self):
            return self._extend_query(super(ContentModelSubview, self).get_query())

        def get_count_query(self):
            return self._extend_query(super(ContentModelSubview, self).get_count_query())

        def _extend_query(self, query):
            container_id = request.args.get('id')
            if container_id is None:
                abort(400, "Container id required")
            return query.filter(ContentModel.container_id == container_id)


**Initialize an extension**

.. code-block:: python

    from flask_admin_subview import Subview

    app = Flask(__name__)
    admin = Admin(app, template_mode="bootstrap3")
    # only supports bootstrap3 mode
    Subview(app, template_mode="bootstrap3")


**Add your subview as a blueprint**

.. code-block:: python

    app = Flask(__name__)
    # ...
    app.register_blueprint(
        ContentModelSubview(Content, db.session, "Content", endpoint="content_subview").
        create_blueprint(admin))


**Prepare container view**

Use helper to display subview in the model's details:

.. code-block:: python

    from flask_admin_subview import SubviewContainerMixin, SubviewEntry

    class ContainerView(SubviewContainerMixin, ModelView):
        can_view_details = True
        subviews = (
            # specify that we need to pass id from the location URL to the subview
            SubviewEntry("/admin/content_subview/", "Content Subview", "id"),
        )


TODO
====

- Add tests
- Add example app code comments
- Add Bootstrap2 templates
- Possibly, support inline edits
- Describe advanced usage
