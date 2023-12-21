from flask import Flask, render_template
from flask_migrate import Migrate
from routes.blueprint import blueprint


def create_app():
    app = Flask(__name__)  # flask app object
    app.config.from_object('config')  # Configuring from Python Files

    return app


app = create_app()  # Creating the app
# Registering the blueprint
app.register_blueprint(blueprint, url_prefix='/')
migrate = Migrate(app)  # Initializing the migration


if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)