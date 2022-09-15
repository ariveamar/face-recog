import json
from flask import Flask, render_template, Response, jsonify
from pymongo import MongoClient
app = Flask(__name__)
client = MongoClient('3349393a5d2a74a16e3a333d17b7e4ece371af465a3c969edff36393be5bac6e', 27017)
db = client.devdb_dpo
dpos = db.dpos

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

@app.route("/")
def index():
    modify_nav("Data Kriminalitas")
    allResult = dpos.find()
    return render_template("layout.html",result=allResult, nav=nav, body="index.html")
@app.route("/identify_faces")
def identify_faces():
    modify_nav("Identifikasi Wajah")
    return render_template("layout.html", nav=nav, body="identify_faces.html")

def modify_nav(path):
    for i, item in enumerate(nav, start=0):
        if item["name"] == path:
            nav[i]["isActive"] = True
        else:
            nav[i]["isActive"] = False

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)