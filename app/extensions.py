from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin


db = SQLAlchemy()
security = Security()
migrate = Migrate()
mail = Mail()
csrf = CSRFProtect()
admin = Admin(template_mode='bootstrap4')
