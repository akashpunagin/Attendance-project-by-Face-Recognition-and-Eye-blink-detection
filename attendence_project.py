import numpy as np
import cv2
import face_recognition as fr
from glob import glob
import pickle
import utility
import define_constants as const

print('-----------------------------------------------------\n')

# Load data from pickle file (n_people)
with open('assets/pickles/n_people.pk', 'rb') as pickle_file:
    n_people_in_pickle = pickle.load(pickle_file)
print(f"Number of files that should be in '{const.PEOPLE_DIR}' directory : {n_people_in_pickle}")

# Read all images
people = glob(const.PEOPLE_DIR + '/*.*')
print(f"Number of files in '{const.PEOPLE_DIR}' directory : {len(people)}")

# Check if number of files in PEOPLE_DIR is same as value in pickle file
if n_people_in_pickle == len(people):
    # Get names
    names = list(map(utility.get_names, people))

    # Get encodings
    face_encode = np.load('assets/face_encodings/data.npy')

    # Initiate Webcam
    print("Initiating camera...\n")

    cap = cv2.VideoCapture(const.n_camera)

    while cap.isOpened():
        # Read Frames
        ret, frame = cap.read()
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get Face locations
        frame_face_loc = fr.face_locations(frame)
        frame_face_encode = fr.face_encodings(frame)

        for index, (loc, encode) in enumerate(zip(frame_face_loc, frame_face_encode)):
            # Compare current encoding with face encodings
            # is_face_same = fr.compare_faces(face_encode, encode)
            score = fr.face_distance(face_encode, encode)
            index_match = np.argmin(score)

            # Check if min(score) is < 0.6
            if np.min(score) < const.face_recognition_threshold:
                frame_current_name = names[index_match]
            else:
                frame_current_name = "Unknown"

            # Draw Reactangle around faces with their names
            cv2.rectangle(frame,(loc[3],loc[0]),(loc[1],loc[2]),(0,0,255),2) # top-right, bottom-left
            cv2.putText(frame,frame_current_name,(loc[3],loc[0]),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)

            # Record Attendence only if score is atmost 0.6
            if np.min(score) < const.face_recognition_threshold:
                utility.record_attendence(frame_current_name)

        cv2.imshow("Webcam (Press q to quit)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print(f"Run encode_faces.py to encode all faces in '{const.PEOPLE_DIR}' directory...")
