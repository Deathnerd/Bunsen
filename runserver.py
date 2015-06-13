#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand
from bunsen.app import create_app, db
from bunsen.settings import Production, Development, Staging
from bunsen.modules.core.members.models import Member
from bunsen.modules.core.pages.models import Page
from flask import g, url_for
from flask.ext.login import current_user

if os.environ.get("BUNSEN_SERVER_ENV", None) == "prod":
    app = create_app(Production)
elif os.environ.get("BUNSEN_SERVER_ENV", None) == "staging":
    app = create_app(Staging)
else:
    app = create_app(Development)


# Before/After request methods
@app.before_request
def load_user():
    g.user = current_user


HERE = os.path.abspath(os.path.dirname(__file__))

manager = Manager(app)


def _make_context():
    """
    Return context dict for a shell session so we can access things
    :return:
    """
    return {'app': app, 'db': db, 'Member': Member, 'Page': Page}


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
