from flask import Flask, render_template, redirect, url_for

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from werkzeug.utils import secure_filename
import os
import detector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Upload')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html', title='Home')


@app.route('/error')
def error():
    return render_template('error.html', title='Error page')


@app.route('/css')
def css():
    return render_template('gallery.css', title='Gallery')


@app.route('/inference')
def inference():
    return render_template('inference.html', title='Inference page')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        if allowed_file(secure_filename(f.filename)):
            if os.path.exists(os.path.join(UPLOAD_FOLDER, "test_pic.png")):
                os.remove(os.path.join(UPLOAD_FOLDER, "test_pic.png"))
            if os.path.exists(os.path.join(UPLOAD_FOLDER, "result_img.png")):
                os.remove(os.path.join(UPLOAD_FOLDER, "result_img.png"))

            f.save(os.path.join(UPLOAD_FOLDER, "test_pic.png"))
            YOLO = detector.detector()
            YOLO.inference_result()
            return redirect(url_for('inference'))
        else:
            return redirect(url_for('error'))

    return render_template('photo.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
