from os import environ
import yaml
from .logger import logger

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


def _load_config(config_file):
    with open(config_file, 'r',encoding='utf8') as f:
        c = yaml.load(f)
    logger.info(c)

    #for k in c.keys():
    #    c[k]['reply'] = cycle(c[k]['reply'])
    return c


app.jinja_env.filters['kst'] = kst_filter


@app.before_first_request
def setup():
    from .models.user import User
    from .models.cheers import Cheerup

    """
    User.metadata.drop_all(bind=db.engine)
    User.metadata.create_all(bind=db.engine)
    Cheerup.metadata.drop_all(bind=db.engine)
    Cheerup.metadata.create_all(bind=db.engine)

    global config
    for v in config.values():
        key = v['key']
        for r in v['reply']:
            c = Cheerup(key, r)
            db.session.add(c)
            print(key, r)
    db.session.commit()
    """


def spin(config_file, host='localhost', port=5000, debug=True):
    global config
    config = _load_config(config_file)
    for bp in blueprints:
        print(bp)
        mod = import_string('geungjungbot.views.%s:mod' % bp)
        app.register_blueprint(mod)

    app.run(host=host, port=port, debug=debug)
