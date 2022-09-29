from flask_cors import CORS
from flask import Flask, render_template, request, redirect
from repository.repository import Repository
from connection import dpos, doh, hiltem
from werkzeug.utils import secure_filename
import requests
import json
import os
import sys
from dotenv import load_dotenv
load_dotenv()
UPLOAD_FOLDER = 'image'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

repo = Repository
nav = [
    {
        "route":"/",
        "name":"Data Kriminalitas",
        "isActive":True
    },
    {
        "route":"/identify_faces",
        "name":"Identifikasi Wajah",
        "isActive":False
    },
    {
        "route":"/input_dpo",
        "name":"Input DPO",
        "isActive":False
    }
]

@app.route("/updatePickle", methods=['POST'])
def updatePickle():
    if request.method == 'POST':
        repo.savePickle(repo)
        return {"messages":"Berhasil update Pickle"}
    else:
        return {"messages":"Gagal update Pickle"}
@app.route("/input_dpo")
def input_dpo():
    modelAttribute = {}
    modify_nav("Input DPO")
    masterDataJenisIdentitasReq = requests.get(os.getenv("MDM_SERVICE_URL")+'/mdm/jenis-identitas')
    masterDataProvinsiReq = requests.get(os.getenv("MDM_SERVICE_URL")+'/mdm/provinsi')
    modelAttribute["masterDataJenisIdentitas"] = json.loads(masterDataJenisIdentitasReq.text)["result"]
    modelAttribute["masterDataProvinsi"] = json.loads(masterDataProvinsiReq.text)["result"]
    modelAttribute["backendURL"] = os.getenv("BACKEND_DPO_SERVICE_URL")
    return render_template("layout.html", nav=nav, body="dpo/input.html", title="Input DPO", modelAttribute=modelAttribute)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/")
def index():
    dataKriminalitas = {}
    modify_nav("Data Kriminalitas")
    dataKriminalitas["dpo"] = dpos
    dataKriminalitas["doh"] = doh
    dataKriminalitas["hiltem"] = hiltem
    return render_template("layout.html", dataKriminal=dataKriminalitas, nav=nav, body="index.html", title="Data Kriminalitas")
@app.route("/identify_faces", methods=['GET'])
def identify_faces():
    modify_nav("Identifikasi Wajah")
    return render_template("layout.html", nav=nav, body="identify_faces.html", title="Identifikasi Wajah")

@app.route("/identify", methods=['POST'])
def identify():
    if request.method == 'POST':
        if 'file' not in request.files:
            return {"result":"file not found"} 

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            # The image file seems valid! Detect faces and return the result.
            return {"result":repo.face_identify(repo, path)} 
    return {"messages":"Method Not Allowed"}

def modify_nav(path):
    for i, item in enumerate(nav, start=0):
        if item["name"] == path:
            nav[i]["isActive"] = True
        else:
            nav[i]["isActive"] = False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)