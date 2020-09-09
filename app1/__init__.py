from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app1.config import configuration

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view='users.login'
login_manager.login_message_category='_info_'
mail = Mail()




def create_app(config_class = configuration):
    app = Flask(__name__)
    app.config.from_object(configuration)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)


    from app1.users.routes import users
    from app1.posts.routes import posts
    from app1.main.routes import main
    from app1.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app
