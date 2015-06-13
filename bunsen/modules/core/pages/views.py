# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from bunsen.modules.core.pages.models import Page

import os

try:
    from bunsen.app import APP_DIR

    static_folder = os.path.join(APP_DIR, 'static')
except ImportError:
    static_folder = "../../../static"

blueprint = Blueprint("pages", __name__, url_prefix="/")


# put dynamic routes here
@blueprint.route("/", defaults={"slug": None})
@blueprint.route("/<string:slug>")
def page(slug):
    # first check for index
    if slug is None:  # if the slug is a None object, then this is the index page
        page = Page.query.filter(Page.is_index == True).filter(Page.active == True).first_or_404()
    else:
        page = Page.query.filter(Page.endpoint == slug).filter(Page.active == True).first()
        if page is None:
            # could not find by endpoint, so find by page slug
            page = Page.query.filter(Page.name == slug).filter(Page.active == True).first_or_404()
    return render_template("public/pages/default_page.html", page=page)


"""
Flask-Admin Model Views
"""

from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose


class PageModelView(ModelView):
    edit_template = "bunsen/pages/edit_page.html"
    list_template = "bunsen/pages/list_pages.html"
    create_template = "bunsen/pages/create_page.html"

    def __init__(self, session, **kwargs):
        super(PageModelView, self).__init__(Page, session, **kwargs)
