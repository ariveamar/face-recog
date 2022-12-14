import face_recognition
import pickle
import numpy as np
import math
from connection import dpos, doh, hiltem
import base64
from bson.objectid import ObjectId
import sys
import urllib.request as ur
class Repository:
    all_face_encodings = {}
    def __init__(self):
        self.all_face_encodings = {}
    def loadPickle(self, path):
        f = open(path, 'rb')
        self.all_face_encodings = pickle.load(f)
        f.close
        return self
    def savePickle(self):
        dpo = dpos.find()
        allPersonDPO = {}
        for item in dpo:
            image = "data:"+item['mimeType']+";base64,"+item['photo']
            decoded= ur.urlopen(image)
            foto = face_recognition.load_image_file(decoded)
            allPersonDPO[str(item["_id"])] = face_recognition.face_encodings(foto)[0]
        f = open('dataset_faces.dat', 'wb')
        pickle.dump(allPersonDPO, f)
        f.close
        return self
    def face_distance_to_conf(face_distance, face_match_threshold=0.8):
        if face_distance > face_match_threshold:
            range = (1.0 - face_match_threshold)
            linear_val = (1.0 - face_distance) / (range * 2.0)
            return linear_val
        else:
            range = face_match_threshold
            linear_val = 1.0 - (face_distance / (range * 2.0))
            return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))
    def face_identify(self, file_image):
        self.loadPickle(self, 'dataset_faces.dat')
        face_names = list(self.all_face_encodings.keys())
        face_encodings = np.array(list(self.all_face_encodings.values()))
        unknown_image = face_recognition.load_image_file(file_image)
        unknown_face = face_recognition.face_encodings(unknown_image)[0]
        face_distances = face_recognition.face_distance(face_encodings, unknown_face)
        listFace = []
        for i, face_distance in enumerate(face_distances, start=0):
            percentage = self.face_distance_to_conf(face_distance=face_distance)
            if percentage > 0.9:
                res = dpos.find_one({"_id":ObjectId(face_names[i])})
                del res["_id"]
                res["kemiripan"] = "{:.2f}".format((percentage* 100.0))+"%" 
                listFace.append(res)
        return listFace
        
    