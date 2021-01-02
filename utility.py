import cv2
import string
from datetime import datetime
from gtts import gTTS
from pygame import mixer
from multiprocessing import Pool
from scipy.spatial import distance as dist
import define_constants as const
import os

# Define helper functions
def get_names(path):
    name = path.split(os.sep)[-1].split('.')[0]
    name = string.capwords(name.replace("_", " "))
    return name

def get_images(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return img

def get_EAR_ratio(eye_points):
    # euclidean distance between two vertical eye landmarks
    A = dist.euclidean(eye_points[1], eye_points[5])
    B = dist.euclidean(eye_points[2], eye_points[4])

    # euclidean distance between horizontal eye landmarks
    C = dist.euclidean(eye_points[0], eye_points[3])

    # Eye Aspect Ratio
    return (A + B) / (2.0 * C)

def check_is_name_recorded(name):
    with open(const.CSV_FILE_PATH, 'r+') as file:
        # Read lines in csv file, except first line
        lines_in_file = file.read().splitlines()[1:]
        # Store only names
        names_in_file = list(map(lambda line : line.split(',')[0], lines_in_file))

        if name in names_in_file:
            return True
        else:
            return False

def record_attendence(frame_current_name):
    with open(const.CSV_FILE_PATH, 'r+') as file:
        # Read lines in csv file, except first line
        lines_in_file = file.read().splitlines()[1:]
        # Store only names
        names_in_file = list(map(lambda line : line.split(',')[0], lines_in_file))

        if not frame_current_name in names_in_file:
            # Create datetime object
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_weekday = now.strftime("%A")
            current_month = now.strftime("%B")
            current_day_of_month = now.strftime("%d")

            # Write time and day details
            file.writelines(f"{frame_current_name},{current_weekday},{current_month},{current_day_of_month},{current_time}\n")
            text_display = f"{frame_current_name}, your attendence is recorded"
            print(text_display)

            if const.text_to_speech:
                pool = Pool(processes=1) # Start a worker processes
                result = pool.apply_async(text_to_speech, [text_display])

def text_to_speech(text):
    # Text to Sppech
    gtts_obj = gTTS(text=text, lang='en', slow=False)
    gtts_obj.save('assets/text_to_speech/text_to_speech.mp3')

    mixer.init()
    mixer.music.load('assets/text_to_speech/text_to_speech.mp3')
    mixer.music.play()
