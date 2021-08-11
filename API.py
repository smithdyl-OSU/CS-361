import img_transformer
from flask import request
from flask import Flask
from flask import send_file

app = Flask(__name__)


@app.route('/', methods=['POST'])
def resize():
    file = request.files['image']
    img = Image.open(file.stream)
    resized_img = image_resize(img)
    return send_file(resized_img, mimetype='resized_image/jpg')
