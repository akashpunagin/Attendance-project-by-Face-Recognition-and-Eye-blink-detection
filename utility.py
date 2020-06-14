import cv2
from datetime import datetime


# Define helper functions
get_names = lambda path : path.split('/')[-1].split('.')[0]

def get_images(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return img

def record_attendence(frame_current_name):
    with open('attendence.csv', 'r+') as file:
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
            print(f"{frame_current_name}, your attendence is recorded")
