from flask_sqlalchemy import SQLAlchemy
from rememberator import create_app


app = create_app()
db = SQLAlchemy(app)
