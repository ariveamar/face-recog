from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from repository.repository import Repository
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
load_dotenv()
client = MongoClient(os.getenv("IP_ADDR_SERVER_MONGO"), int(os.getenv("PORT_SERVER_MONGO")))

devdb_dpo = client.devdb_dpo
dpos = devdb_dpo.dpos

devdb_doh = client.devdb_doh
doh = devdb_doh.doh

devdb_hiltem = client.devdb_hiltem
hiltem = devdb_hiltem.hiltem

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
    }
]
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/")
def index():
    modify_nav("Data Kriminalitas")
    allResult = dpos.find()
    return render_template("layout.html",result=allResult, nav=nav, body="index.html", title="Data Kriminalitas")
@app.route("/identify_faces", methods=['GET', 'POST'])
def identify_faces():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.

            return {
                    "name":repo.face_identify(repo, file)
                }
    modify_nav("Identifikasi Wajah")
    return render_template("layout.html", nav=nav, body="identify_faces.html", title="Identifikasi Wajah")

def modify_nav(path):
    for i, item in enumerate(nav, start=0):
        if item["name"] == path:
            nav[i]["isActive"] = True
        else:
            nav[i]["isActive"] = False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)