from img_transformer import image_resize
from flask import request
from flask import Flask
from flask import send_file
from PIL import Image

app = Flask(__name__)


@app.route('/', methods=['POST'])
def resize():
    print(request.files)
    file = request.files['image']
    img = Image.open(file.stream)
    resized_img = image_resize(img)
    return send_file(resized_img, mimetype='resized_image/jpg')
