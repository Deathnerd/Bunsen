# -*- coding: utf-8 -*-
import datetime as dt

from bunsen.database import Column, db, Model, ReferenceCol, relationship, SurrogatePK


class Page(SurrogatePK, Model):
    __tablename__ = "pages"
    name = Column(db.String(255), nullable=False)
    content = Column(db.Text, default="Content coming soon!")
    created = Column(db.DateTime, default=dt.datetime.utcnow)
    active = Column(db.Boolean, default=True)
    updated = Column(db.DateTime, default=dt.datetime.utcnow)
    endpoint = Column(db.String(255), nullable=True)  # if None, then this is the index
    is_index = Column(db.Boolean, default=False)

    def __init__(self, name="", **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return "<Page {name}>".format(name=self.name)