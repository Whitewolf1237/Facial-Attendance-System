import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "database url"  # Your Firebase Database URL
})

ref = db.reference('Students')

# Example student data
data = {
    "852741": {
        "name": "Emly Blunt",
        "major": "Economics",
        "starting_year": 2021,
        "total_attendance": 12,
        "standing": "B",
        "year": 1,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    "963852": {
        "name": "Elon Musk",
        "major": "Physics",
        "starting_year": 2020,
        "total_attendance": 7,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    "324928": {
        "name": "Nitin Rai",
        "major": "AIML",
        "starting_year": 2020,
        "total_attendance": 9,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    }
}

# Make sure the local storage folder exists
if not os.path.exists('local_storage'):
    os.makedirs('local_storage')

# Saving the data locally in a file before pushing to Firebase (optional step for backup)
with open('local_storage/student_data.txt', 'w') as file:
    for student_id, student_info in data.items():
        file.write(f"{student_id}: {student_info}\n")

# Push data to Firebase Database
for key, value in data.items():
    ref.child(key).set(value)

print("Data added to Firebase and saved locally.")
