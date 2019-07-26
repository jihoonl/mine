from sqlalchemy.sql.expression import func, select

from ..run import db
from ..logger import logger


class CheerData(object):

    def __init__(self, obj):
        self._obj = obj

    def __call__(self):
        return self._obj


class Cheerup(db.Model):
    __tablename__ = 'cheerup'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(30), nullable=False)
    _cheerup = db.Column(db.PickleType, nullable=False)

    def __init__(self, type, cheerup):
        self.type = type
        self._cheerup = CheerData(cheerup)

    def __repr__(self):
        return '<Cheerup id={}, cheerup'.format(self.id, self._cheerup)

    @property
    def cheerup(self):
        return self._cheerup


def get_types():
    types = db.session.query(Cheerup.type).distinct().all()
    return [t[0] for t in types]


def get_message(typ):
    return Cheerup.query.filter_by(type=typ).order_by(
        func.random()).first().cheerup()
