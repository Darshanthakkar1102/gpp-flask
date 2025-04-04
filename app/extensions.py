from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_security import Security

db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()
bootstrap = Bootstrap()
migrate = Migrate()
security = Security()
