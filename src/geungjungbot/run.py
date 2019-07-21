from os import environ

import pytz
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string

from .views import blueprints

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI',
                                                    'sqlite:////tmp/test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS', False)
db = SQLAlchemy(app)
db.engine.raw_connection().connection.text_factory = str


def kst_filter(dt, format_='%Y-%m-%d %H:%M:%S %Z'):
    tz = pytz.timezone('Asia/Seoul')
    return dt.astimezone(tz).strftime(format_)


app.jinja_env.filters['kst'] = kst_filter

for bp in blueprints:
    print(bp)
    mod = import_string('geungjungbot.views.%s:mod' % bp)
    app.register_blueprint(mod)


@app.before_first_request
def setup():
    from .models.user import User
    User.metadata.drop_all(bind=db.engine)
    User.metadata.create_all(bind=db.engine)


def spin(config_file, host='localhost', port=5000, debug=True):
    app.run(host=host, port=port, debug=debug)
