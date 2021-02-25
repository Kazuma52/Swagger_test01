from flask import Flask, render_template, request, send_from_directory, jsonify
import os

from flasgger import Swagger
from flasgger.utils import swag_from

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'storage'
app.config["SWAGGER"] = {"title": "Swagger-UI", "uiversion": 2}
ALLOWED_EXTENSIONS = {'.json'}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}

swagger = Swagger(app, config=swagger_config)

def check_extension(incoming_file):
    file_ext = os.path.splitext(incoming_file)[1]
    if file_ext in ALLOWED_EXTENSIONS:
        return True
    else: 
        return False

@app.route('/get/')
def home():
    return render_template('index.html')


@app.route('/keep/', methods=['GET'])
@app.route('/keep/', methods=['POST'])
@swag_from("simple_specs.yml")
def store():
    if request.method == 'POST':
        f = request.files['file']                   #name of file with extention
        filename = f.filename
        #f.save(os.path.join(app.config['UPLOAD_PATH'], filename))   #This isn't working
        if check_extension(filename)==True:
            return json.dumps(filename+" was stored")
        else:
            return json.dumps(filename+" is not a json")
    else:
        return json.dumps("only POST requests")


if __name__=='__main__':
    app.run(debug= True)