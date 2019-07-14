def get_heart(num=1):
    return u'\u2764\ufe0f'.encode('utf-8') * num


def build_response(message):
    # message contains only string data.
    if isinstance(message, unicode):
        response = {"message": {"text": message.encode('utf-8')}}
    elif isinstance(message, str):
        response = {"message": {"text": message}}
    elif isinstance(message, dict):
        response = {
            "message": {
                "text": message['text'].encode('utf-8'),
                "photo": {
                    "url": message['photo'].encode('utf-8'),
                    "width": 640,
                    "height": 480
                }
            }
        }
    else:
        response = {"message": {"text": "에러났어. " + str(type(message))}}

    return response
