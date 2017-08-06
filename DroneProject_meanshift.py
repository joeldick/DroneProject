import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

if __name__ == "__main__":
    video_capture = cv2.VideoCapture('drone_video.avi')
    #video_capture = cv2.VideoCapture('short_drone_video.avi')

    while video_capture.isOpened():
        # grabs and retrieves the next frame
        (ret, frame) = video_capture.read()
        if ret:

            frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_orange = np.array([18, 64, 50])
            upper_orange = np.array([35, 255, 255])

            mask = cv2.inRange(frame_HSV, lower_orange, upper_orange)
            frame_masked = cv2.bitwise_and(frame, frame, mask=mask)

            #plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            #plt.show()
            cv2.imshow('frame', frame)
            cv2.imshow('mask', mask)
            cv2.imshow('res', frame_masked)

        if cv2.waitKey(int(1)) == ord('q') or cv2.getWindowProperty('frame', 0):
            break

    video_capture.release()
    cv2.destroyAllWindows()
