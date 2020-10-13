import http
import re
from dataclasses import dataclass
from http import HTTPStatus
from typing import List

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
    req = request.json
    code = req.get('code')
    debug = req.get('debug')
    input_ = req.get('input')
    breakpoints = req.get('breakpoints')
    print(_parse_breakpoints(breakpoints, code))
    try:
        snapshots = api.run(code, debug=debug, input_=input_)
    except Exception as err:
        return jsonify(statusCode=HTTPStatus.INTERNAL_SERVER_ERROR, message=str(err))
    snapshots_dicts = [serializer.serialize_snashot(ss) for ss in snapshots]
    return jsonify(statusCode=http.HTTPStatus.OK, snapshots=snapshots_dicts)


@dataclass
class Breakpoint:
    current_lineno: int
    original_lineno: int
    instr: str


def _parse_breakpoints(breakpoints: List[int], code: str):
    new_breakpoints = []
    code_lines = code.split('\n')
    code_with_breakpoint_markers = []
    for lineno, line in enumerate(code_lines):
        if lineno in breakpoints:
            code_with_breakpoint_markers.append(f'{lineno}*{line}')
        else:
            code_with_breakpoint_markers.append(line)
    code_with_breakpoint_markers = '\n'.join(code_with_breakpoint_markers)
    cleaned_code = re.sub(r'\n+', '\n', code_with_breakpoint_markers)
    cleaned_code_lines = cleaned_code.split('\n')
    for lineno, line in enumerate(cleaned_code_lines, start=1):
        match = re.match(r'(\d+)\*(.*)$', line)
        if match:
            breakpoint = Breakpoint(current_lineno=lineno, original_lineno=int(match.group(1)), instr=match.group(2))
            new_breakpoints.append(breakpoint)
    return new_breakpoints
