import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import api

UPLOAD_FOLDER = "data"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'obj', 'fbx', 'json', 'ttl', 'ply'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variables
referencePosition = 0
errorRadius = 0
dirname = os.path.dirname(__file__)

# The main page to show stuff 
@app.route("/")
def index():
    return "This is the Votenet server"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a sub selection of the data with given global coordinates
@app.route("/boundingbox", methods=['POST'])
def boundingbox():

    print(request.files)

    # check if the post request has the file part
    if 'file' not in request.files:
        print('No file part in files')
        return "No File Provided"

    uploaded_files = request.files.getlist("file")
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if len(uploaded_files) == 0:
        print('File array is empty')
        return "File array is empty"
    else:
        savePath = os.path.join(dirname,app.config['UPLOAD_FOLDER'])
        for file in uploaded_files:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filePath = os.path.join(savePath, filename)
                file.save(filePath)
                print("saved file @" + filePath)

                # Run the votenet Detector

                # Get the bounding boxes as an array
                api.get_json_bounding_boxes(filePath)

        return "<h2>Succes!</h2>"
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7000, debug=False)