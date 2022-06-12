import connexion
from swagger_ui_bundle import swagger_ui_3_path

# DB Connection
from database.db import db
from database.db import migrate


def create_app(config_filename=None):
    app = connexion.App(
        __name__, specification_dir="./", options={"swagger_path": swagger_ui_3_path}
    )
    flask_app = app.app

    #CONFIG
    if config_filename is not None:
        flask_app.config.from_object(config_filename)
    else:
        flask_app.config.from_object("config.development")

    #DB
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)

    app.add_api("swagger.yml")

    return app.app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5050, debug=True)
