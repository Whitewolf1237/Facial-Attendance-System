import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "Your Database URL"  # Your Firebase Database URL
})

# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []

for path in pathList:
    # Read the image
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
    # Save the images locally (no upload to Firebase Storage)
    localFilePath = f'local_storage/{path}'
    if not os.path.exists('local_storage'):
        os.makedirs('local_storage')
    cv2.imwrite(localFilePath, cv2.imread(os.path.join(folderPath, path)))
    # Here you can save image paths or names to Firebase DB if needed
    ref = db.reference('students')
    ref.child(studentIds[-1]).set({
        'imagePath': localFilePath
    })

print(studentIds)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

# Save the encoding data locally as well
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")
