import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

if __name__ == "__main__":
    video_capture = cv2.VideoCapture('drone_video.avi')

    # get first frame
    (ret, frame) = video_capture.read()

    #set initial location of orange ball
    y_init, h, x_init, w = (408, 20, 680, 20)
    track_window = (x_init, y_init, w, h)

    # select range of image around orange golfball
    roi = frame[y_init:y_init+h, x_init:x_init+w]

    # convert to HSV so we can see what the HSV for orange is
    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    #hsv_plot = plt.imshow(roi_hsv)
    #plt.show()

    # create a mask for only orange pixels
    # pixel range was figured out by looking at plot above
    # [Actually, the purpose of this line is not supposed to be
    # to filter out only orange pixels, but to filter out
    # low light images. The range should be [0,60,32] - [180,255,255]
    # or some other such high pass filter
    mask = cv2.inRange(roi_hsv, np.array([0, 60, 32]), np.array([180, 255, 255]))
    #mask_plot = plt.imshow(mask)
    #plt.show()

    # get histogram of masked image
    # use range of 180 because we are picking out the Hue (0-180)
    roi_hist = cv2.calcHist([roi_hsv], [0], mask, [180], [0,180])
    # normalize histogram to 255
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    #hist_plot = plt.hist(roi_hist)
    #plt.show()

    # We now have the histogram of the orange golf ball.
    # Read successive frames and take the backprojection
    # of this histogram on each frame to detect golf ball.
    #
    # Then, use meanShift to move frame to area of frame
    # that matches the backprojection best

    while video_capture.isOpened():
        (ret, frame) = video_capture.read()

        # here we take the backprojection
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        backprojection = cv2.calcBackProject([frame_hsv], [0], roi_hist, [0, 180], 1)

        # here we apply meanshift
        # termination criteria is 10 iterations or move by at least 1 pixel
        termination_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        ret, track_window = cv2.CamShift(backprojection, track_window, termination_crit)

        # now we have our new track window
        # draw it on the frame
        x, y, w, h = track_window
        img_rect = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
        cv2.imshow('img_rect', img_rect)

        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()
    video_capture.release()
