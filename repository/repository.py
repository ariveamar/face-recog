import face_recognition
import pickle
import numpy as np
import math
from connection import dpos, doh, hiltem
import base64
from bson.objectid import ObjectId
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
            image_path = "image/"+str(item["_id"])+"."+str(item["mimeType"]).split("/")[1]
            fh = open(image_path, "wb")
            fh.write(base64.b64decode(item["photo"]))
            foto = face_recognition.load_image_file(image_path)
            allPersonDPO[str(item["_id"])] = face_recognition.face_encodings(foto)[0]
        f = open('dataset_faces.dat', 'wb')
        pickle.dump(allPersonDPO, f)
        f.close
        return self
    def face_distance_to_conf(face_distance, face_match_threshold=0.6):
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
        unknown_face = face_recognition.face_encodings(unknown_image)
        for i, face in enumerate(face_encodings, start=0):
            face_distances = face_recognition.face_distance(unknown_face, face)
            percentage = self.face_distance_to_conf(face_distance=face_distances)
            if percentage > 0.9:
                res = dpos.find_one({"_id":ObjectId(face_names[i])})
                del res['_id']
                del res['_class']
                del res['photo']
                return res
        return {"messages":"Unknow Faces"}
        
    