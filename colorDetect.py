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
    video_capture = cv2.VideoCapture(filename)

    # get information about video
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print("frames per second: " + str(int(fps)))

    num_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    print("number of frames: " + str(int(num_frames)))

    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frameCounter = 0

    while video_capture.isOpened():
        # grabs and retrieves the next frame
        (ret, frame) = video_capture.read()
        if ret:
            frameCounter += 1

            frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # orange range is for golf ball in close up video
            lower_orange = np.array([24, 112, 230])
            upper_orange = np.array([31, 170, 255])

            mask = cv2.inRange(frame_HSV, lower_orange, upper_orange)
            frame_masked = cv2.bitwise_and(frame, frame, mask=mask)

            #plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            #plt.show()
            cv2.imshow('frame', frame)
            cv2.imshow('mask', mask)
            cv2.imshow('res', frame_masked)

        if cv2.waitKey(int(1000/fps)) == ord('q') or cv2.getWindowProperty('frame', 0):
            break

    print("number of frames played: " + str(frameCounter))
    video_length = frameCounter/fps
    print("length: " + str(video_length) + " seconds")
    video_capture.release()
    cv2.destroyAllWindows()
