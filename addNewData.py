import cv2
import os
import firebase_admin
from firebase_admin import credentials, db
import face_recognition
import pickle

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")  # Replace with your Firebase credentials
firebase_admin.initialize_app(cred, {
    'databaseURL': 'Database url',  # Replace with your Firebase Realtime Database URL
})

# Initialize the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()  # Exit if the camera cannot be opened

# Create a folder to store student images if it doesn't exist
image_folder = 'Images'
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Function to register student data and capture their photo
def register_student():
    print("Please enter student details:")

    student_id = input("Student ID: ")

    # Capture photo for the student
    print("Please look at the camera for your photo.")
    print("Press 'Space' to take the photo, 'Esc' to cancel.")

    count = 0
    student_image_path = f"{image_folder}/{student_id}.png"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            continue

        # Display the captured frame
        cv2.imshow("Register Student", frame)

        # Wait for key press
        key = cv2.waitKey(1) & 0xFF

        # Capture photo when 'Space' key is pressed
        if key == 32:  # Spacebar
            cv2.imwrite(student_image_path, frame)  # Save the image locally
            print(f"Photo for student {student_id} captured successfully!")
            break

        # Cancel photo capture if 'Esc' key is pressed
        elif key == 27:  # Escape key
            print("Photo capture cancelled.")
            student_image_path = None
            break

    cv2.destroyAllWindows()

    if student_image_path:
        name = input("Student Name: ")
        major = input("Major: ")
        year = input("Year: ")
        start_year = input("Starting Year: ")

        # Create student data to upload to Firebase Realtime Database
        student_data = {
            "name": name,
            "major": major,
            "year": year,
            "start_year": start_year,
            "image_path": student_image_path,  # Store the local image path
            "total_attendance": 0,
            "standing": "N/A",  # Default value
            "last_attendance_time": "2024-01-01 00:00:00"  # Default value
        }

        # Upload student data to Firebase Realtime Database
        ref = db.reference(f'Students/{student_id}')
        ref.set(student_data)

        # Update encoding with new student's data
        update_encoder(student_id)

        print(f"Student {name} registered successfully!")

# Function to update encoder with the new student data
def update_encoder(new_student_id):
    print("Updating Encoder...")

    # Load the existing encoder and student data
    try:
        with open("EncodeFile.p", 'rb') as file:
            encodeListKnownWithIds = pickle.load(file)
        encodeListKnown, studentIds = encodeListKnownWithIds
    except FileNotFoundError:
        encodeListKnown = []
        studentIds = []

    # Load the newly added student image
    student_image_path = f"{image_folder}/{new_student_id}.png"
    img = cv2.imread(student_image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img_rgb)[0]  # Get face encoding

    # Append the new student's encoding and ID to the lists
    encodeListKnown.append(encode)
    studentIds.append(new_student_id)

    # Save the updated encoder to a file
    with open("EncodeFile.p", 'wb') as file:
        pickle.dump([encodeListKnown, studentIds], file)

    print("Encoder updated successfully!")

# Run the registration function
register_student()

# Release the camera and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
