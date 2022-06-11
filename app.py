import connexion
from swagger_ui_bundle import swagger_ui_3_path


def create_app(config_filename=None):
    app = connexion.App(
        __name__, specification_dir="./", options={"swagger_path": swagger_ui_3_path}
    )

    app.add_api("swagger.yml")

    return app.app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5050, debug=True)
