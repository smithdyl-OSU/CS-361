from img_transformer import image_resize
from flask import request
from flask import Flask
from flask import send_file
from PIL import Image

app = Flask(__name__)


UPLOAD_FOLDER = '/nfs/stak/users/smithdyl/CS361/CS-361/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST'])
def resize():
    print(request.files)
    file = request.files['image']
    print(file)
    resized_img = image_resize(file)
    return send_file(resized_img, mimetype='resized_image/jpg')
