# -*- coding: utf-8 -*-
import os


class Base():
    """Base Config"""
    # General App
    ENV = os.environ.get('BUNSEN_SERVER_ENV', 'dev')
    SECRET_KEY = os.environ.get('BUNSEN_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    # SERVER_NAME = "example.com"

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}?charset=utf8".format(
        os.environ.get('BUNSEN_DATABASE_USER', 'bunsen'),
        os.environ.get('BUNSEN_DATABASE_PASS', 'pass'),
        os.environ.get('BUNSEN_DATABASE_HOST', 'localhost'),
        os.environ.get('BUNSEN_DATABASE_NAME', 'bunsen'))

    # Bcrypt
    BCRYPT_LOG_ROUNDS = 13

    # Debug Toolbar
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # WTForms
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('BUNSEN_WTF_CSRF_SECRET_KEY', 'secret-key')
    RECAPTCHA_PUBLIC_KEY = os.environ.get('BUNSEN_RECAPTCHA_PUBLIC_KEY', 'public-key')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('BUNSEN_RECAPTCHA_PRIVATE_KEY', 'private-key')


class Production(Base):
    """Production Config"""
    DEBUG = False
    DEBUG_TB_ENABLED = False


class Development(Base):
    """Development Config"""
    # General App
    DEBUG = True

    # SQLAlchemy
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Base.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)

    # Debug Toolbar
    DEBUG_TB_ENABLED = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True

    # ASSETS_DEBUG = True

    # WTF-Forms


class Staging(Base):
    """Staging Config"""
    # General App
    TESTING = True
    DEBUG = True

    # Bcrypt
    BCRYPT_LOG_ROUNDS = 1

    # WTForms
