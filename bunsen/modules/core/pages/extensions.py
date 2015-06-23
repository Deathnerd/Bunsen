# -*- coding: utf-8 -*-
from flask import url_for
from bunsen.modules.core.pages.models import Page
from bunsen.modules.core.pages.exceptions import BunsenPageBuildError


def generate_jinja_extensions(app):
    @app.context_processor
    def utility_processors():
        def bunsen_page(endpoint, **values):
            """
            Finds a page in the Bunsen CMS database and constructs a URL for it.

            First sends all arguments through <pre>url_for("pages.page", **values)</pre>
            to get the correct routing information from Flask for the Pages module.

            Then, if the endpoint requested is index, first attempts to find an index page in the
            database. If index is not requested, then it first searches through the database by endpoint
            and failing that, searches by name. If all fails, then raise a BunsenPageBuildError.

            It will also attach any extra keyword parameters passed to it as url arguments
            :return:
            """

            # get the url from the stock url_for. This is mostly to get those sweet sweet params
            default_url = url_for("pages.page", **values)
            params = None
            if "?" in default_url:
                default_url, params = default_url.split("?")
            # get the pages in the database

            if endpoint.lower() == "index":
                db_page = Page.query.filter(Page.is_index == True).first()
            else:
                db_page = Page.query.filter(Page.endpoint == endpoint).first()
                if db_page is None:
                    db_page = Page.query.filter(Page.name == endpoint).first()
            if db_page is None:
                raise BunsenPageBuildError("The page {endpoint} could not be found in the Bunsen database", errors=["Foo"])

            # page is in the database. Get the URL
            # If the page in the database is an index page, then just return a bare index route
            if db_page.is_index:
                ret_val = default_url
            else:
                if default_url[-1] != "/":
                    default_url += "/"
                ret_val = "{d}{p}".format(d=default_url, p=db_page.endpoint)

            # Append the parameters
            if params is not None:
                ret_val += "?{}".format(params)

            return ret_val

        return dict(bunsen_page=bunsen_page)
