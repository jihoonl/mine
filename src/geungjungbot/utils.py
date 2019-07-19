def get_heart(num=1):
    return u'\u2764\ufe0f'.encode('utf-8') * num


def build_response(message):
    # message contains only string data.
    if isinstance(message, unicode):
        response = {"simpleText": {"text": message.encode('utf-8')}}
    elif isinstance(message, str):
        response = {"simpleText": {"text": message}}
    elif isinstance(message, dict):
        response = {
            "simpleImage": {
                "altText": message['text'].encode('utf-8'),
                "imageUrl": message['photo'].encode('utf-8'),
                "width": 640,
                "height": 480
            }
        }
    else:
        response = {"simpleText": {"text": "error. " + str(type(message))}}

    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                response
            ]
        }
    }
    return response
