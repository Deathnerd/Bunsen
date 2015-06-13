# -*- coding: utf-8 -*-
"""
    flaskext.dynforms
    ~~~~~~~~~~~~~~~~~

    Description of the module goes here...

    :copyright: (c) 2015 by Deathnerd.
    :license: BSD, see LICENSE for more details.
"""

"""
TODO: make everything!
"""

__default_validators__ = ["Email", "EqualTo", "IPAddress", "Length", "NumberRange", "Optional", "Required", "Regexp",
                          "URL", "AnyOf", "NoneOf"]
__default_fields__ = ["Boolean", "Date", "DateTime", "Decimal", "File", "Float", "Hidden", "Integer", "Password",
                      "Radio", "Select", "SelectMultiple", "Submit", "TextArea", "String", "Form"]
from flask_wtf import Form
from flask_wtf.form import _Auto


class DynForms(object):
    def __init__(self, db=None, app=None):
        self.db = db
        self.app = app
        if app is not None and db is not None:
            self.init_app(app, db)

    def init_app(self, app, db):
        self.db = db
        self.app = app
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

        # try:
        #     from .models import Validator, Forms, Field
        #
        #     if len(Validator.query.all()) == 0:  # Check for validators in the database
        #         # generate the tables
        #         from .setup import generate_all
        #
        #         generate_all()
        # except:
        #     raise TableGenerationError("There was an error generating one of the tables")

    def teardown(self, exception):
        # do teardown stuff here
        pass


class DynamicForm(Form):
    """
    The workhorse class of the DynForms extension. Extends the WTForms module by
    providing methods to store a form in a database and generate a Form object based on
    those values. Usage as follows:

    myform = DynamicForm("formName") # tries to pull a form from the database with the given name or generates it if not exists


    """

    def __init__(self, formname="", formdata=_Auto,*args, **kwargs):
        """
                The constructor method takes care of loading a form from the database
                :param formname: The name of the form to pull from the database
                :param formid: The id of the form in the database to pull from
                :param args:
                :param kwargs:
                """
        from bunsen.modules.core.dynforms.models import Forms

        if formname != "":
            self.form_model_object = Forms.query.filter_by(name=formname).first()
        else:
            raise Exception("No valid form identifier given")
        if self.form_model_object is None:
            # The record didn't exist, so we'll make a new one
            self.form_model_object = Forms(formname)

        # Call the super's init method to treat this as a form
        super(DynamicForm, self).__init__(*args, **kwargs)