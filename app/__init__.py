import os
from flask import Flask
from config import Config


def create_app(config_class=Config):
    """
    Application factory function.

    Create and configure the application.
    :return: app instance
    """
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    # ensure the folders exists for database, images, and invoices
    try:
        os.makedirs(app.instance_path)
        os.makedirs(app.config['UPLOAD_FOLDER'])
        os.makedirs(app.config['INVOICE_DIR'])
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import main
    app.register_blueprint(main.bp)

    return app
