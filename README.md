# Attendence project using Face Recognition

#### Basic python packages used
* OpenCV
* NumPy
* tqdm
* pickle
* glob
* string
* scipy

### Packages for Face Recognition and Eye Blink Detection
* cmake
* dlib
* face_recognition

### Packages for Text to Speech
* gTTS
* pygame


### Installing dlib on Ubuntu, [More](https://www.pyimagesearch.com/2018/01/22/install-dlib-easy-complete-guide/)
* $ sudo apt-get update
* $ sudo apt-get install build-essential cmake
* $ sudo apt-get install libopenblas-dev liblapack-dev
* $ sudo apt-get install libx11-dev libgtk-3-dev
* $ sudo apt-get install python python-dev python-pip
* $ sudo apt-get install python3 python3-dev python3-pip

## How to run
* Store all images **with one face** in 'people' directory. *Some images are avaibable*
* Run enode_faces.py
* Run attendence_project.py
* Edit define_constants.py file **if required**

### Output
##### First attendence
![Elon Musk](/README_media/Screenshot_elon_musk.png "Elon Musk")

##### Second Attendence
![David Gilmour](/README_media/Screenshot_david_gilmour.png "David Gilmour")

##### .csv file can be viewed in spreadsheets
![Spreadsheet](/README_media/Screenshot_spreadsheet.png "Spreadsheet")

# Eye Blink Update :
### After this update, attendence is recorded only after the person blinks a certain amount of time.

## Result
##### Click on the GIF to open the video in YouTube
[![Result](/README_media/attendence_project_video.gif "Result")](https://www.youtube.com/watch?v=uW48UC3WEos)
