import os

from flask import Blueprint, url_for
from wtforms.widgets import HTMLString


class Subview(object):
    JINJA_NAME = "Subview"
    JS_FILE_NAME = "subview.js"
    CSS_FILE_NAME = "subview.css"
    DEFAULT_STATIC_URL_PREFIX = "/static/admin/subview/js"
    DEFAULT_JS_PATH = "{}/{}".format(DEFAULT_STATIC_URL_PREFIX, JS_FILE_NAME)

    def __init__(self, app=None, bp=None, static_url_prefix=DEFAULT_STATIC_URL_PREFIX):
        self.app = None
        self.bp = bp
        self.static_url_prefix = static_url_prefix
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        if self.bp is None:
            self.bp = Blueprint("flask_admin_subview", __name__, template_folder="templates",
                                static_url_path=self.static_url_prefix,
                                static_folder=os.path.join(os.path.dirname(os.path.realpath(__file__)), "static"))
        self.app.register_blueprint(self.bp)
        self.app.jinja_env.globals[self.JINJA_NAME] = self

    def css_html(self):
        return HTMLString('<link href="{}" rel="stylesheet">'.format(url_for("{}.static".format(self.bp.name),
                                                                             filename=self.CSS_FILE_NAME)))
