from os import environ

import pytz
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string

from .views import blueprints

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = environ.get('DATABASE_URI',
                                                    'sqlite:////tmp/test.db')
db = SQLAlchemy(app)


def kst_filter(dt, format_='%Y-%m-%d %H:%M:%S %Z'):
    tz = pytz.timezone('Asia/Seoul')
    return dt.astimezone(tz).strftime(format_)


app.jinja_env.filters['kst'] = kst_filter

for bp in blueprints:
    mod = import_string('geungjungbot.views.%s:mod' % bp)
    app.register_blueprint(mod)

if __name__ == '__main__':
    app.run(debug=True)
