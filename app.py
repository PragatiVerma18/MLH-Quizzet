import os
from flask import Flask, render_template, redirect, url_for
from flask.globals import request
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader

# Constants
UPLOAD_FOLDER = './pdf/'


# Init an app object
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    """ The landing page for the app """
    return render_template('index.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    UPLOAD_STATUS = False
    if request.method == 'POST':
        try:
            uploaded_file = request.files['file']
            # Make directory to store uploaded files
            if not os.path.isdir('./pdf'):
                os.mkdir('./pdf')
            # Save uploaded file
            uploaded_file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename)))
            UPLOAD_STATUS = True

            # Identify file type and other stuff
            uploaded_content = None
            file_exten = uploaded_file.filename.rsplit('.', 1)[1].lower()
            if file_exten == 'pdf':
                # TODO: Move PDF2Text conversion to another file
                print('PDF detected')
                with open(os.path.join(
                        app.config['UPLOAD_FOLDER'], secure_filename(uploaded_file.filename)), 'rb') as pdf_file:
                    pdf_reader = PdfFileReader(pdf_file)
                    uploaded_content = pdf_reader.getPage(0).extractText()
                    print(uploaded_content)
            else:
                # Read text file and store contents
                pass

        except Exception as e:
            print(e)
    return render_template('quiz.html', uploaded=UPLOAD_STATUS, pdftext=uploaded_content)


if __name__ == "__main__":
    app.run(debug=True)
