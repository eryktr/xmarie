from flask import Flask, request, jsonify
from xmarievm.parsing import parser
from xmarievm.runtime.streams.input_stream import BufferedInputStream
from xmarievm.runtime.streams.output_stream import OutputStream
from xmarievm.runtime.vm import MarieVm

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/run', methods=['POST'])
def run():
    if request.method != 'POST':
        raise ValueError('Invalid request type')
    code = request.json.get('code')
    vm = MarieVm(memory=[0] * 1024, input_stream=BufferedInputStream(''), output_stream=OutputStream(), stack=[])
    print(code)
    prog = parser.parse(code)
    vm.execute(prog)
    return jsonify(isError=False, message='Success', statusCode=200, AC=vm.AC)
