# -*- coding: utf-8 -*-
from bunsen.modules.core.dynforms.dynforms import __default_fields__, __default_validators__

""" :type : SQLAlchemy """
from bunsen.app import db

"""
Many-to-many relationship between validators and fields
"""
validators = db.Table('validators-pivot',
                      db.Column('field_id', db.Integer, db.ForeignKey("dynforms-fields.id")),
                      db.Column('validator_id', db.Integer, db.ForeignKey("dynforms-validators.id")))

class Forms(db.Model):
    __tablename__ = "dynforms-forms"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    fields = db.relationship('Field', backref="form", lazy="dynamic")
    action = db.Column(db.Text, default="self")
    method = db.Column(db.Enum("GET", "POST"), default="POST")

    def __init__(self, name, fields=None, action="self", method="POST", **kwargs):
        db.Model.__init__(self, name=name, fields=fields, action=action, method=method, **kwargs)

    def __repr__(self):
        return "<Form {form_name}>".format(form_name=self.name)


class Field(db.Model):
    """
    See http://wtforms.simplecodes.com/docs/0.6/fields.html
    TODO: Provide widget field
    """
    __tablename__ = "dynforms-fields"
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('dynforms-forms.id'))
    # These are all the types of fields that WTForms supplies
    type = db.Column(db.Enum(*__default_fields__),
                     nullable=False, default="Text")
    label = db.Column(db.String(128), default='')
    default = db.Column(db.String(128), nullable=True)
    placeholder = db.Column(db.String(128), nullable=True)
    validators = db.relationship('Validator', secondary=validators, backref=db.backref('fields', lazy='dynamic'))
    html_id = db.Column(db.String(25), nullable=True)
    description = db.Column(db.Text, default='')

    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)

    def __repr__(self):
        if len(self.label) > 0:
            return "<Form Field {id}:{label}>".format(id=self.id, label=self.label)
        return "<Form Field {id}>".format(id=self.id)


class Validator(db.Model):
    """
    See http://wtforms.simplecodes.com/docs/0.6/validators.html for full list of validators
    """
    __tablename__ = "dynforms-validators"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(*__default_validators__), unique=True)
    message = db.Column(db.Text, nullable=True)
    options = db.Column(db.Text, default="{}")  # shouldn't be a string of json, but this will do for now

    def __init__(self, name, *args, **kwargs):
        db.Model.__init__(self, name=name, *args, **kwargs)

    def __repr__(self):
        return "<Validator {name}>".format(name=self.name)