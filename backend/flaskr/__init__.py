import os
from typing import Any

from flask import Flask
from flask_cors import CORS


def create_app(test_config: dict[str, Any] | None = None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/", methods=["GET"])
    def status():
        return "The server has been initialized successfully."

    from . import db

    db.init_app(app)
    app.register_blueprint(db.bp)

    return app
