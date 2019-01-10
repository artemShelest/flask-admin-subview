import os

from flask import Blueprint, url_for
from wtforms.widgets import HTMLString


class Subview(object):
    EXT_NAME = "subview"
    JINJA_NAME = "Subview"
    JS_FILE_NAME = "subview.js"
    CSS_FILE_NAME = "subview.css"
    DEFAULT_STATIC_URL_PREFIX = "/static/admin/subview"
    DEFAULT_JS_PATH = "{}/js/{}".format(DEFAULT_STATIC_URL_PREFIX, JS_FILE_NAME)

    def __init__(self, app=None, bp=None, static_url_prefix=DEFAULT_STATIC_URL_PREFIX, template_mode=None):
        """
        Construct Subview helper object.
        :param app: Flask application instance, pass None to postpone initialization
        :param bp: Flask Blueprint instance, pass None for automatic instantiation
        :param static_url_prefix: static files URL prefix
        :param template_mode: Flask-Admin template mode, pass None to infer from the first found Flask-Admin instance.
        """
        self.bp = bp
        self.template_mode = template_mode
        self.static_url_prefix = static_url_prefix
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if self.template_mode is None:
            if not hasattr(app, 'extensions') or app.extensions.get("admin") is None:
                raise RuntimeError("Flask-Admin extension not found. Either specify template mode explicitly, or "
                                   "initialize after Flask-Admin initialization.")
            admin = app.extensions["admin"]
            if len(admin) > 1:
                raise RuntimeError("More than one Flask-Admin instances found, unable to infer template mode. Please, "
                                   "specify it explicitly.")
            self.template_mode = admin[0].template_mode
        # TODO: Implement Bootstrap2 support
        if self.template_mode != "bootstrap3":
            raise NotImplementedError("Only Bootstrap3 is supported")
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        if self.EXT_NAME in app.extensions:
            raise RuntimeError("Subview instance already initialized.")
        app.extensions[self.EXT_NAME] = self
        if self.bp is None:
            self.bp = Blueprint("flask_admin_subview",
                                __name__,
                                template_folder=os.path.join("templates", self.template_mode),
                                static_url_path=self.static_url_prefix,
                                static_folder=os.path.join(os.path.dirname(os.path.realpath(__file__)), "static"))
        app.register_blueprint(self.bp)
        app.jinja_env.globals[self.JINJA_NAME] = self

    def css_html(self):
        return HTMLString('<link href="{}" rel="stylesheet">'.format(url_for("{}.static".format(self.bp.name),
                                                                             filename=self.CSS_FILE_NAME)))

    def js_url(self):
        return url_for("{}.static".format(self.bp.name), filename=self.JS_FILE_NAME)
