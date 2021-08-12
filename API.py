from img_transformer import image_resize
from flask import request
from flask import Flask
from flask import send_file
from PIL import Image
import os

app = Flask(__name__)


UPLOAD_FOLDER = '/nfs/stak/users/smithdyl/CS361/CS-361/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST'])
def resize():
    print(request.files)
    file = request.files['image']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    print(file)
    resized_img = image_resize(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    print(resized_img)
    return send_file('new_image.png', mimetype='image/png')
