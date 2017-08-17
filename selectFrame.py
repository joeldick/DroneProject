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

    while True:
        num_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if num_frames is 0:
            print("Video has no frames.")
            break
        try:
            start_frame = int(input("Type starting frame [0 - " + str(num_frames - 1) + "]. -1 to quit: "))
        except:
            start_frame = 0
        if start_frame == -1:
            break

        video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        ret, frame = video_capture.read()

        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.show(block=False)
        time.sleep(2)
        plt.close()

    video_capture.release()
