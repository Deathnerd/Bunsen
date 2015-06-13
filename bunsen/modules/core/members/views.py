# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from flask.ext.login import login_required
import os

try:
    from bunsen.app import APP_DIR

    static_folder = os.path.join(APP_DIR, 'static')
except ImportError:
    static_folder = "../../../static"

blueprint = Blueprint("members", __name__, url_prefix='/members',
                      static_folder=static_folder)


@blueprint.route("/")
@login_required
def members():
    return render_template("public/members/members.html")


from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from bunsen.modules.core.members.models import Member, Role
from bunsen.extensions import bcrypt

"""
Backend admin views here
"""


class MembersView(BaseView):
    @expose("/members")
    def members_index(self):
        return self.render("bunsen/members/index.html")


class MembersModelView(ModelView):
    list_template = "bunsen/members/list_members.html"
    edit_template = "bunsen/members/edit_member.html"

    def __init__(self, session, **kwargs):
        super(MembersModelView, self).__init__(Member, session, **kwargs)

    def on_model_change(self, form, member, is_created):
        """
        When the model in Bunsen is changed (created or modified), do these actions. In this case,
        Flask-Admin is not aware of our password hashes by default, so we have to add that in ourselves

        :param form:
        :param member:
        :param is_created:
        :return:
        """
        member.password = bcrypt.generate_password_hash(form.password.data)


class RolesModelView(ModelView):
    list_template = "bunsen/members/list_roles.html"
    edit_template = "bunsen/members/edit_role.html"

    def __init__(self, session, **kwargs):
        super(RolesModelView, self).__init__(Role, session, **kwargs)