import http
from http import HTTPStatus

from flask import Flask, request, jsonify
from flask_cors import CORS
from xmarievm import api
from xmarievm.parsing.parser import ParsingError
from xmarievm.runtime import snapshot_maker

import actions
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

    try:
        if action == actions.DEBUG:
            hit = vm_mgr.debug(token, code, input_, breakpoints)
            if hit:
                return jsonify(
                    statusCode=http.HTTPStatus.OK,
                    snapshot=serializer.serialize_snashot(hit.snapshot),
                    breakpoint=serializer.serialize_breakpoint(hit.breakpoint)
                )
            else:
                return jsonify(
                    statusCode=http.HTTPStatus.OK,
                    status='terminated',
                    snapshot=serializer.serialize_snashot(snapshot_maker.make_snapshot(vm_mgr.vms[token]))
                )
        if action == actions.CONTINUE:
            hit = vm_mgr.continue_debug(token)
            if hit:
                return jsonify(
                    statusCode=http.HTTPStatus.OK,
                    status='ok',
                    breakpointHit=True,
                    snapshot=serializer.serialize_snashot(hit.snapshot),
                    breakpoint=serializer.serialize_breakpoint(hit.breakpoint),
                )
            return jsonify(
                statusCode=http.HTTPStatus.OK,
                status='ok',
                breakpointHit=False,
            )
        if action == actions.STEP:
            try:
                hit = vm_mgr.debugstep(token)
                return jsonify(
                    status='hit',
                    statusCode=http.HTTPStatus.OK,
                    current_lineno=hit.current_lineno,
                    original_lineno=hit.original_lineno,
                    snapshot=serializer.serialize_snashot(hit.snapshot),
                )
            except RuntimeError:
                return jsonify(
                    status='terminated',
                )
        else:
            snapshot = vm_mgr.run(token, code, input_)

    except (ParsingError, SyntaxError) as err:
        return jsonify(statusCode=HTTPStatus.BAD_REQUEST, status='parsingError', message=str(err))
    return jsonify(statusCode=http.HTTPStatus.OK, snapshots=[serializer.serialize_snashot(snapshot)])
