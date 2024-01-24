from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists
from sqlalchemy import func, exc
from flask_migrate import Migrate
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    db_name='db.sqlite'
    if database_exists('sqlite:///'+db_name):
        print(db_name + " already exists")
    else:
        print(db_name + " does not exist, will create " + db_name)
        # this is needed in order for database session calls (e.g. db.session.commit)
        with app.app_context():
            try:
                db.create_all()
            except exc.SQLAlchemyError as sqlalchemyerror:
                print("got the following SQLAlchemyError: " + str(sqlalchemyerror))
            except Exception as exception:
                print("got the following Exception: " + str(exception))
            finally:
                print("db.create_all() in __init__.py was successfull - no exceptions were raised")
    return app

app = create_app()
migrate = Migrate(app)
if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)