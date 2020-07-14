from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from acsystem.config import Config
from flask_wtf.csrf import CSRFProtect

bcrypt = Bcrypt()
db = SQLAlchemy()
csrf_token = CSRFProtect()

login_manager = LoginManager()

login_manager.login_view ='users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app,db)
    migrate.init_app(app)
    login_manager.init_app(app)
    csrf_token.init_app(app)

    from acsystem.user.routes import users
    from acsystem.company.routes import company
    from acsystem.main.routes import main
    from acsystem.customer.routes import customers
    from acsystem.supplier.routes import suppliers
    from acsystem.groupledger.routes import groupledgers
    from acsystem.product.routes import products
    from acsystem.transactions.routes import transactions
    from acsystem.tax.routes import taxes
    app.register_blueprint(users)
    app.register_blueprint(company)
    app.register_blueprint(main)
    app.register_blueprint(customers)
    app.register_blueprint(suppliers)
    app.register_blueprint(groupledgers)
    app.register_blueprint(products)
    app.register_blueprint(transactions)
    app.register_blueprint(taxes)

    return app





