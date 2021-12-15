import io
import os
import time
from unitex_tagger import TextTagger
from text_extractor import PDFExtractor
from werkzeug.utils import secure_filename
from gunicorn.app.base import BaseApplication
from flask import Flask, render_template, request, redirect, flash, Markup, jsonify

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'pdf'}
pdf_file = None


def clean_directory(working_file):
    """ Remove files from given directory """
    folder = 'static/uploads/'
    for filename in os.listdir(folder):
        if filename == working_file:
            file_path = os.path.join(folder, filename)
            try:
                os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


class GunicornApplication(BaseApplication):

    def __init__(self, application, config=None):
        self.__application = application
        self.__config = config or {}

        super(GunicornApplication, self).__init__()

    def load_config(self):
        config = {key: value for key, value in self.__config.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.__application


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def convert_pdf(file_path, remove_images=False):
    """
    Converts PDF to text. See PDFExtractor class for more information.
    """
    extractor = PDFExtractor(file_path)
    extractor._pdf_to_html(remove_images)


def tag_text():
    """
    Tags text using Unitex grammars. See TextTagger class for more information.
    """
    # Text tagging process.
    # Highlight grammar is a composed graph containing text-matching grammars
    # and their corresponding assigned tags.
    tagger = TextTagger('config/unitex-example.yaml')
    tagger.import_text('full_pdf.html')
    pdf_html = tagger.tag_text('config/graphs/highlight.fst2')
    # Structures matches to pass them in HTML template.
    return (tagger.matched, Markup(pdf_html))


@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialisation for initial empty template
    pdf_file = None
    file_name = None
    text_content = [""]
    matches = {'sent': {'': ''}, 'entity': {'': ''}, 'idx': {'': ''}}
    pdf = None
    remove_images = False
    # Gets file uploaded from webapp
    if request.method == 'POST':
        # Checks for file import success
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        # Gets files uploaded
        uploaded_file = request.files['file']
        file_name = uploaded_file.filename  # Name of the file 'name.pdf'
        # Handles 'file is not a PDF'
        if not allowed_file(uploaded_file.filename):
            print(uploaded_file.filename)
            print('File is not a PDF')
            return redirect(request.url)
        # Gets secure name of PDF for rendering
        filename = secure_filename(uploaded_file.filename)
        # Saves and applies processing to PDF
        if uploaded_file.filename != '':
            pdf_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(pdf_file)
            if request.form.get('rmv_img'):
                print("removing IMG")
                remove_images = True
            convert_pdf(pdf_file, remove_images)
        matches,  pdf = tag_text()
    # Renders webapp.
    return render_template('index.html', text=text_content,
                           matches=matches, file_path=pdf_file,
                           file_name=file_name, clean=clean_directory, pdf=pdf)
                           
                           
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
                           
@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'               


@app.route('/clean', methods=['GET', 'POST'])
def clean_pdf():
    to_clean = request.args.get('param_file')
    time.sleep(5)
    return jsonify(result=clean_directory(to_clean))
    


if __name__ == '__main__':
    GunicornApplication(app).run()
    # app.run(debug=False)
