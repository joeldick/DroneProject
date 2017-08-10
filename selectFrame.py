import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

if __name__ == "__main__":
    video_capture = cv2.VideoCapture('drone_video.avi')
    #video_capture = cv2.VideoCapture('person_drone_video.avi')

    num_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    print("number of frames: " + str(int(num_frames)))

    frame_selection = 0
    while True:
        try:
            frame_selection = int(input("Select frame: "))
        except:
            break

        video_capture.set(cv2.CAP_PROP_POS_FRAMES, int(frame_selection))
        (ret, frame) = video_capture.read()

        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.show()

    video_capture.release()
