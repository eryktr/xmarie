import http
from http import HTTPStatus

from flask import Flask, request, jsonify
from flask_cors import CORS
from xmarievm import api

import serializer
from vm_manager import VmManager

app = Flask(__name__)
cors = CORS(app)

if __name__ == '__main__':
    app.run(debug=True)

vm_mgr = VmManager()


@app.route('/run', methods=['POST'])
def run():
    if request.method != 'POST':
        raise ValueError('Invalid request type')
    req = request.json
    code = req.get('code')
    debug = req.get('debug')
    input_ = req.get('input')
    token = req.get('token')
    action = req.get('action')
    breakpoints = req.get('breakpoints')
    print(token)
    print(action)
    try:
        snapshots = api.run(code, debug=debug, input_=input_, breakpoints=breakpoints)
    except Exception as err:
        return jsonify(statusCode=HTTPStatus.INTERNAL_SERVER_ERROR, message=str(err))
    snapshots_dicts = [serializer.serialize_snashot(ss) for ss in snapshots]
    return jsonify(statusCode=http.HTTPStatus.OK, snapshots=snapshots_dicts)
