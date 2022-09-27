import urllib.request as ur
from PIL import Image, ImageShow
import face_recognition
from connection import dpos, doh, hiltem
from bson.objectid import ObjectId
person = dpos.find_one({"_id":ObjectId("632bd86bb69fba2a741ddc4f")})
image = "data:"+person['mimeType']+";base64,"+person['photo']
decoded= ur.urlopen(image)
image_loaded = face_recognition.load_image_file(decoded)
face_locations = face_recognition.face_locations(image_loaded)

for face_location in face_locations:
    top, right, bottom, left = face_location
    coordinates = image_loaded[top:bottom, left:right]
    face = Image.fromarray(coordinates)
    ImageShow.show(face)
