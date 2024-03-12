import os, tempfile, base64
from flask import Flask, render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from image_gen import image_gen
from io import BytesIO

app = Flask(__name__)
#UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route("/")
def hello_world():
    return render_template("index.html")

#TODO error management
@app.route("/up", methods=['GET', 'POST'])
def infos_upload():
    photos = {}
    if request.method == 'POST':
        expected_files = ['old_pic1', 'old_pic2', 'new_pic']
        if request.files and all(file in expected_files for file in request.files):
            for i in range(0, len(expected_files)):
                image = request.files[expected_files[i]]
                if (valid := validate_image(image)):
                    photos[expected_files[i]] = image

                if not valid:
                    return "<p>error</p>"
                
            return end_friendship(photos, request.form)
        return redirect(request.base_url)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(image):
    if image.filename == '':
        return False
    if image and allowed_file(image.filename):
        return True

def end_friendship(photos, data):
    final_image = image_gen(photos['new_pic'], photos['old_pic1'], photos['old_pic2'], data['old_name'], data['new_name'])

    buffered = BytesIO()
    final_image.save(buffered, format="PNG")
    image_b64 = base64.b64encode(buffered.getvalue())

    return render_template("goodbye.html", img_data=image_b64)