import http
from http import HTTPStatus

from flask import Flask, request, jsonify
from flask_cors import CORS
from xmarievm import api

import serializer

app = Flask(__name__)
cors = CORS(app)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/run', methods=['POST'])
def run():
    if request.method != 'POST':
        raise ValueError('Invalid request type')
    code = request.json.get('code')
    debug = request.json.get('debug')
    try:
        snapshots = api.run(code, debug=debug)
    except Exception as err:
        return jsonify(statusCode=HTTPStatus.INTERNAL_SERVER_ERROR, message=str(err))
    snapshots_dicts = [serializer.serialize_snashot(ss) for ss in snapshots]
    print(snapshots)
    return jsonify(statusCode=200, snapshots=snapshots_dicts)
