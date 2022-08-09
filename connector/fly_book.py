from flask import request, Blueprint
import json
import requests


fb = Blueprint('flybook', __name__)


@fb.route("/auto_response")
def do_response():
    print(request.data)
    url = ""

    return {
        'code': '200',
        'data': '',
        'message': '成功'
    }


if __name__ == '__main__':
    do_response()