import face_recognition
import pickle
import numpy as np
import math
class Repository:
    all_face_encodings = {}
    def __init__(self):
        self.all_face_encodings = {}
    def loadPickle(self, path):
        f = open(path, 'rb')
        self.all_face_encodings = pickle.load(f)
        f.close
        return self
    def savePickle(self, path):
        f = open(path, 'wb')
        pickle.dump({}, f)
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
            face_distances = face_recognition.face_distance(face, unknown_face)
            percentage = self.face_distance_to_conf(face_distance=face_distances)
            if percentage > 0.9:
                return face_names[i]
        return "Unknow Faces"
        
    