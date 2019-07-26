# -*- coding: utf-8 -*-

from ..run import db
from ..logger import logger


class User(db.Model):
    __tablename__ = 'users'

    _user_id = db.Column(
        db.String(66), primary_key=True, unique=True, nullable=False)
    _name = db.Column(db.String(64))

    def __init__(self, user_id, name):
        self._user_id = user_id.decode('utf-8')
        logger.info(name)
        self._name = name.strip().decode('utf-8')

    def __repr__(self):
        return '<User id={}, name={}>'.format(self.user_id, self.name)

    def __str__(self):
        return self.__repr__()

    @property
    def name(self):
        return self._name.encode('utf-8')

    @property
    def user_id(self):
        return self._user_id.encode('utf-8')


def get_user(json):
    user_id = json['userRequest']['user']['id']
    user = User.query.filter_by(_user_id=user_id).first()
    return user
