from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from acsystem.config import Config

bcrypt = Bcrypt()
db = SQLAlchemy()

manager = Manager()
# migrate = Migrate()
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()

login_manager.login_view ='user.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app,db)
    migrate.init_app(app)
    login_manager.init_app(app)

    from acsystem.user.routes import users
    from acsystem.company.routes import company
    from acsystem. main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(company)
    app.register_blueprint(main)

    return app

