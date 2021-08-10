import img_transformer.py
from flask import request
from flask import Flask
from flask import send_file

app = Flask(__name__)


@app.route('/resize', methods=['POST'])
def resize():
    param = request.args
    filename = image_resize(param)
    return send_file(filename, mimetype='resized_image/jpg')


@app.route('/trans', methods=['POST'])
def trans():
    param = request.args
    filename = image_trans(param)
    return send_file(filename, mimetype='transparent_image/png')
