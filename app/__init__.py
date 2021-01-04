from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# импортировать биб-ку Migrate для работы с миграциями
from flask_migrate import Migrate

app = Flask(__name__,
            static_url_path='',
            static_folder='static')


# подключаем базу данных к приложению
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../carsharing.sqlite"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# создаем базу данных
db = SQLAlchemy(app)

# создаем объект для работы с миграциями
migrate = Migrate(app, db)


from app import routes
from app import models
