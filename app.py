from flask import Flask, render_template
from flask.globals import request
from werkzeug.utils import secure_filename

# Init an app object
app = Flask(__name__)

UPLOAD_PATH = './pdf/'


@app.route('/')
def index():
    """ The landing page for the app """
    return render_template('index.html')  # render foe template from ./templates


@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        try:
            uploaded_file = request.files['file']
            uploaded_file.save(
                UPLOAD_PATH + secure_filename(uploaded_file.filename))
            uploaded = True
            return render_template('index.html', uploaded=uploaded)
        except Exception as e:
            return 'failed to upload file'


if __name__ == "__main__":
    app.run(debug=True)
