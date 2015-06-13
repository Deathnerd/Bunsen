# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import os
from flask import Flask

from .settings import Production
from .assets import assets
from .extensions import bcrypt, cache, db, login_manager, migrate, debug_toolbar, bunsen_admin, request_errors
from bunsen.modules.core import pages

from bunsen.modules.core.members.views import MembersModelView, RolesModelView
from bunsen.modules.core.pages.views import PageModelView

APP_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app(config_object=Production):
    """An application factory, as explained here:
     http://flask.pocoo.org/docs/patterns/appfactories/
    :param config_object: The configuration object to use.
    """
    app = Flask(__name__, template_folder=os.path.join(APP_DIR, "templates"))
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_bunsen_admin(MembersModelView, RolesModelView, PageModelView, session=db.session)

    configure_login()
    return app


def register_extensions(app):
    """
    Given an app object, initialize the application extensions
    :param app: The current application
    :returns None:
    """
    assets.init_app(app)
    bunsen_admin.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    # request_errors.init_app(app)
    return None


def register_blueprints(app):
    """
    Given an app object, initialize the blueprints
    :param app: The current application
    :return None:
    """
    app.register_blueprint(pages.views.blueprint)
    return None


def configure_login():
    login_manager.login_view = "public.login"


def register_bunsen_admin(*args, **kwargs):
    """
    Takes in any number of ModelViews and adds them to Bunsen's backend interface
    a la Flask-Admin
    :param args:
    :param kwargs:
    :return:
    """
    for view in args:
        bunsen_admin.add_view(view(kwargs['session']))
    return None