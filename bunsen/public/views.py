# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, session)
from flask.ext.login import login_user, login_required, logout_user

from ..extensions import login_manager
from ..user.models import User
from ..public.forms import LoginForm
from ..user.forms import RegisterForm
from ..utils import flash_errors
from ..database import db

blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/")
def index():
    """
    The public home page. Make it purty and awesome!
    """
    return render_template("public/home.html")


@blueprint.route("/login/", methods=["GET", "POST"])
def login():
    """
    The public home page. Make it purty and awesome!
    """
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/login.html", form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.index'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                               email=form.email.data,
                               password=form.password.data,
                               active=True)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.index'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
