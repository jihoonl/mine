# -*- coding: utf-8 -*-

from ..run import db
from ..logger import logger


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(
        db.String(66), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(64))

    def __init__(self, user_id, name):
        self.user_id = user_id
        logger.info(name)
        self.name = name.strip()

    def __repr__(self):
        return '<User id={}, name={}>'.format(self.user_id, self.name)


def get_user(json):
    user_id = json['userRequest']['user']['id']
    user = User.query.filter_by(user_id=user_id).first()
    return user
