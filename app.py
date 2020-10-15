import os
from flask import Flask, render_template, redirect, url_for
from flask.globals import request
from werkzeug.utils import secure_filename
from workers import pdf2text, txt2questions

# Constants
UPLOAD_FOLDER = './pdf/'


# Init an app object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@ app.route('/')
def index():
    """ The landing page for the app """
    return render_template('index.html')


@ app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """ Handle upload and conversion of file + other stuff """

    UPLOAD_STATUS = False
    questions = dict()

    # Make directory to store uploaded files, if not exists
    if not os.path.isdir('./pdf'):
        os.mkdir('./pdf')

    if request.method == 'POST':
        try:
            # Retrieve file from request
            uploaded_file = request.files['file']
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                secure_filename(
                    uploaded_file.filename))
            file_exten = uploaded_file.filename.rsplit('.', 1)[1].lower()

            # Save uploaded file
            uploaded_file.save(file_path)
            # Get contents of file
            uploaded_content = pdf2text(file_path, file_exten)
            questions = txt2questions(uploaded_content)

            # File upload + convert success
            if uploaded_content is not None:
                UPLOAD_STATUS = True
        except Exception as e:
            print(e)
    return render_template(
        'quiz.html',
        uploaded=UPLOAD_STATUS,
        questions=questions,
        size=len(questions))


@app.route('/result', methods=['POST', 'GET'])
def result():
    correct_q = 0
    for k, v in request.form.items():
        correct_q += 1
    return render_template('result.html', total=5, correct=correct_q)


if __name__ == "__main__":
    app.run(debug=True)
