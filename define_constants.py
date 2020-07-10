# DEFINE PATHS
PEOPLE_DIR = "people"
CSV_FILE_PATH = "results/attendence.csv"

# DEFINE IF YOU WANT TEXT TO SPEECH
text_to_speech = True

# DEFINE CAMERA NUMBER
n_camera = 0

# FACE RECOGNITION CONSTANTS
face_recognition_threshold = 0.5 # Lesser the value, more accurate the result
n_face_encoding_jitters = 50
default_face_box_color = (0,0,255)
success_face_box_color = (0,255,0)
unknown_face_box_color = (0,0,0)
text_in_frame_color = (0,0,255)

# EYE BLINK DETECTION CONSTANTS
n_min_eye_blink = 2
n_max_eye_blink = 5
eye_color = (255, 0, 0)
EAR_ratio_threshold = 0.3 # (EAR - Eye Aspect Ratio)
min_frames_eyes_closed = 3
