from flask import Flask, url_for
from flask_security import roles_required
from elasticsearch import Elasticsearch

import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler

import os
import base64

from .helpers import conf


abs_path = os.path.abspath(os.path.dirname(__file__))

STATIC_FOLDER = os.path.join(abs_path, 'public', 'dist', 'assets')
TEMPLATE_FOLDER = os.path.join(abs_path, 'public', 'dist', 'templates')


def create_app():
    # Initiating the flask app
    app = Flask(__name__,
               static_folder=STATIC_FOLDER,
               template_folder=TEMPLATE_FOLDER)

    # Loading the config file
    app.config.from_object('config.DevelopmentConfig')
    #app.config.from_object('config.ProductionConfig')

    # Adding the template and static folder paths to the config
    app.config['TEMPLATE_FOLDER'] = TEMPLATE_FOLDER
    app.config['STATIC_FOLDER'] = STATIC_FOLDER

    # Adding jinja extensions
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.jinja_env.add_extension('jinja2.ext.do')

    # Setting up error logging
    if not app.debug:
        # Sending emails on errors
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ERRORS_MAIL'], subject='Failure in bqlatastaq.com',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # Logging to file on info logs
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=8589934592,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Server startup')

    # Adding extensions
    from .extensions import db, security, migrate, mail, csrf, admin
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)
    admin.init_app(app)

    # Setting up Flask-Security-Too
    from .forms import SignupFormExtension
    from flask_security import SQLAlchemySessionUserDatastore
    from .models import User, Role
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security.init_app(app, user_datastore, confirm_register_form=SignupFormExtension)

    # Registering Blueprints
    from .views import main, blog, admin_extension
    app.register_blueprint(main)
    app.register_blueprint(blog)
    app.register_blueprint(admin_extension)

    # Setting Up Custom Errorhandlers
    from .views.main import not_found, bad_request, server_error
    app.register_error_handler(404, not_found)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(500, server_error)

    # Setting Up Elasticsearch
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])

    # Protecting Admin Index
    @app.before_first_request
    def restrict_admin_url():
        endpoint = 'admin.index'
        url = url_for(endpoint)
        admin_index = app.view_functions.pop(endpoint)

        @app.route(url, endpoint=endpoint)
        @roles_required('admin')
        def secure_admin_index():
            return admin_index()

    # Registering custom jinja filters
    @app.template_filter('titlize')
    def titlize_filter(s):
        return str(s).replace('_', ' ').capitalize()

    @app.template_filter('classify')
    def classify_filter(s):
        return str(s).replace(' ', '-').lower()

    @app.template_filter('str')
    def str_filter(s):
        return str(s)

    # Adding to the Jinja context
    @app.context_processor
    def context_processor():
        context = {
            'conf': conf,
        }
        return context


    return app

