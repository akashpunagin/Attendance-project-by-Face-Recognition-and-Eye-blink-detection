import numpy as np
import cv2
import face_recognition as fr
from glob import glob
import pickle
import utility
import random
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
    print("\nInitiating camera...\n")
    cap = cv2.VideoCapture(const.n_camera)

    # Constants for eye blink detection
    eye_blink_counter = 0
    eye_blink_total = 0
    random_blink_number = random.randint(const.n_min_eye_blink,const.n_max_eye_blink)
    frame_current_name = None

    while cap.isOpened():
        # Read Frames
        ret, frame = cap.read()
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get Face locations, landmarks and encodings
        frame_face_loc = fr.face_locations(frame)
        frame_face_landmarks = fr.face_landmarks(frame, frame_face_loc)
        frame_face_encode = fr.face_encodings(frame, frame_face_loc)

        # Iterate through locations, landmarks and encodings
        for index, (loc, encode, landmark) in enumerate(zip(frame_face_loc, frame_face_encode, frame_face_landmarks)):

            # Find index match
            # is_face_same = fr.compare_faces(face_encode, encode)
            score = fr.face_distance(face_encode, encode)
            index_match = np.argmin(score)

            # Check if min(score) is < face_recognition_threshold
            if np.min(score) < const.face_recognition_threshold:
                # Store name temporarily to check if frame_current_name matches with temp_name
                temp_name = frame_current_name
                # Store new name
                frame_current_name = names[index_match]
            else:
                frame_current_name = "Unknown"

            # If frame_current_name is Unknown don't detect eye (and record attendence)
            if not frame_current_name == "Unknown":
                # Eye blink detection
                left_eye_points = np.array(landmark['left_eye'], dtype=np.int32)
                right_eye_points = np.array(landmark['right_eye'], dtype=np.int32)

                # EAR_left = get_EAR_ratio(left_eye)
                # EAR_right = get_EAR_ratio(right_eye)
                EAR_avg = ( utility.get_EAR_ratio(left_eye_points) + utility.get_EAR_ratio(right_eye_points) ) / 2

                # Check if EAR ratio is less than threshold
                if EAR_avg < const.EAR_ratio_threshold:
                    eye_blink_counter += 1
                else:
                    # Check if counter is greater than min_frames_eyes_closed threshold
                    if eye_blink_counter >= const.min_frames_eyes_closed:
                        eye_blink_total += 1

                    # Reset eye blink counter
                    eye_blink_counter = 0

                # If temp_name doesn't matches with frame_current_name, reset eye_blink_total and set new random_blink_number
                if temp_name != frame_current_name:
                    eye_blink_total = 0
                    random_blink_number = random.randint(const.n_min_eye_blink,const.n_max_eye_blink)

                # Set messages and face box color
                blink_message = f"Blink {random_blink_number} times, blinks:{eye_blink_total}"
                # If name is recorded, display Next person, else don't display anything
                if utility.check_is_name_recorded(frame_current_name):
                    # attendence_message = f"{frame_current_name} your attendence is already recorded"
                    attendence_message = "Next Person"
                else:
                    attendence_message = ""
                face_box_color = const.default_face_box_color

                # If random_blink_number and total blink number matches, then record attendence
                if random_blink_number == eye_blink_total:

                    # Record Attendence only if score is atmost 0.6
                    if np.min(score) < const.face_recognition_threshold:
                        utility.record_attendence(frame_current_name)
                        face_box_color = const.success_face_box_color # Set face box color to green for one frame
                        # Reset random_blink_number, and eye blink constants
                        random_blink_number = random.randint(const.n_min_eye_blink,const.n_max_eye_blink)
                        eye_blink_total = 0
                        eye_blink_counter = 0

                # Draw Eye points and display blink_message and attendence_message
                cv2.polylines(frame, [left_eye_points], True, const.eye_color , 1)
                cv2.polylines(frame, [right_eye_points], True, const.eye_color , 1)
                cv2.putText(frame,blink_message,(10,50),cv2.FONT_HERSHEY_PLAIN,1.5,const.text_in_frame_color,2)
                cv2.putText(frame,attendence_message,(20,450),cv2.FONT_HERSHEY_PLAIN,2,const.text_in_frame_color,2)
            else:
                # Set face_box_color for unknown face
                face_box_color = const.unknown_face_box_color

            # Draw Reactangle around faces with their names
            cv2.rectangle(frame,(loc[3],loc[0]),(loc[1],loc[2]),face_box_color,2) # top-right, bottom-left
            cv2.putText(frame,frame_current_name,(loc[3],loc[0]-3),cv2.FONT_HERSHEY_PLAIN,2,const.text_in_frame_color,2)

        # Display frame
        cv2.imshow("Webcam (Press q to quit)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print(f"Run encode_faces.py to encode all faces in '{const.PEOPLE_DIR}' directory...")
