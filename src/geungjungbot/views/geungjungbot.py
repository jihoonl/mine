from flask import Blueprint, jsonify, make_response, request
import traceback

from ..logger import logger
from ..utils import build_response

mod = Blueprint('gb', __name__)


@mod.route('/keyboard', method=['GET'])
def received_keyboard():
    logger.info('Received keyboard')
    logger.info(request.json)
    message = {'type': 'text'}
    return make_response(jsonify(message), 200)


@mod.route('/message', methods=['POST'])
def received_message():
    logger.info("Received Message")
    logger.info(request.json)

    raw_content = request.json['content']
    content = raw_content.encode('utf-8')
    logger.info(content)

    try:
        message = '훙항힝항홍항항히아하이항'
    except Exception as e:
        logger.error(e)
        traceback.print_exc(file=logger.error)
        message = '에러났어.. %s' % e

    response = build_response(message)
    logger.info(response)

    return make_response(jsonify(response), 200)
