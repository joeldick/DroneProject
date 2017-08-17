import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
from tkinter import Tk
from tkinter import filedialog

if __name__ == "__main__":
    # ask user to choose file
    Tk().withdraw()
    filename = filedialog.askopenfilename()
    print("filename: " + filename)
    video_capture = cv2.VideoCapture(filename)

    # get information about video
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print("frames per second: " + str(int(fps)))

    num_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    print("number of frames: " + str(int(num_frames)))

    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frameCounter = 0

    screen_width = Tk().winfo_screenwidth()
    screen_height = Tk().winfo_screenheight()

    while video_capture.isOpened():
        # grabs and retrieves the next frame
        ret, frame = video_capture.read()
        if ret:
            frameCounter += 1
            frame_resized = cv2.resize(frame, (screen_width,screen_height))
            cv2.imshow('frame', frame_resized)
        key = cv2.waitKey(1)
        if key == ord('q') or cv2.getWindowProperty('frame', 0):
            break
        elif key == ord('p'):
            print("Frame: " + str(video_capture.get(cv2.CAP_PROP_POS_FRAMES)))
            plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            plt.show(block=False)
            time.sleep(2)
            plt.close()

    print("number of frames played: " + str(frameCounter))
    video_length = frameCounter/fps
    print("length: " + str(video_length) + " seconds")
    video_capture.release()
    cv2.destroyAllWindows()
