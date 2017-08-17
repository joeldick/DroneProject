import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import Tk
from tkinter import filedialog

if __name__ == '__main__':
    # ask user to choose file
    Tk().withdraw()
    filename = filedialog.askopenfilename()
    print("filename: " + filename)
    video_capture = cv2.VideoCapture(filename)

    # get resolution of original video
    width_original = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height_original = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # get resolution of user's display
    screen_width = Tk().winfo_screenwidth()
    screen_height = Tk().winfo_screenheight()
    # calculate conversion factor
    screen_to_original_width = width_original/screen_width
    screen_to_original_height = height_original / screen_height

    # ask user to choose tracking algorithm
    algorithm = int(input("Select tracking method - Meanshift(1), Camshift(2), MIL(3), KCF(4): "))
    while True:
        if algorithm == 1:
            print("Chose meanshift")
            break
        elif algorithm == 2:
            print("Chose camshift")
            break
        elif algorithm == 3:
            print("Chose MIL")
            break
        elif algorithm == 4:
            print("Chose KCF")
            break
        else:
            print("Invalid selection")

    while True:
        # ask user for which frame to start from
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

        # read first frame
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        ret, frame = video_capture.read()

        if not ret:
            print("Not able to read file.")
            continue

        # ask user to select object to track
        print("Select object to track")
        frame_resized = cv2.resize(frame, (screen_width, screen_height))
        x, y, w, h = cv2.selectROI(frame_resized, False)
        cv2.destroyAllWindows()
        # do some math to convert coordinates from resized resolution to original resolution
        x = x*screen_to_original_width
        y = y*screen_to_original_height
        w = w*screen_to_original_width
        h = h*screen_to_original_height

        if algorithm == 1 or algorithm == 2:
            print("Running Meanshift/Camshift...")

            bbox = (int(x), int(y), int(w), int(h))
            roi = frame[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]

            # convert to HSV color space
            roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            # Filter out low light pixels (lower than 60/255 saturation and 32/255 value)
            mask = cv2.inRange(roi_hsv, np.array([0, 60, 32]), np.array([180, 255, 255]))
            # get histogram of masked image and normalize it to 255
            roi_hist = cv2.calcHist([roi_hsv], [0], mask, [180], [0, 180])
            cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

            # Set termination criteria of meanshift/camshift to 10 iterations or moved by at least 1 pixel
            termination_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

            while video_capture.isOpened():
                ret, frame = video_capture.read()
                if not ret:
                    break

                # here we take the backprojection
                frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                backprojection = cv2.calcBackProject([frame_hsv], [0], roi_hist, [0, 180], 1)

                # here we apply meanshift/camshift
                if algorithm == 1:
                    ret, bbox = cv2.meanShift(backprojection, bbox, termination_crit)
                elif algorithm == 2:
                    ret, bbox = cv2.CamShift(backprojection, bbox, termination_crit)

                # now we have our new track window
                # draw it on the frame
                x, y, w, h = bbox
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), 255, 2)
                frame_resized = cv2.resize(frame, (screen_width, screen_height))
                cv2.imshow('frame', frame_resized)

                if cv2.waitKey(1) == ord('q'):
                    break
                elif cv2.waitKey(1) == ord('p'):
                    print("Frame: " + str(video_capture.get(cv2.CAP_PROP_POS_FRAMES)))
                    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    plt.show()
        elif algorithm == 3 or algorithm == 4:
            # create tracker
            if algorithm == 3:
                tracker = cv2.Tracker_create("MIL")
            elif algorithm == 4:
                tracker = cv2.Tracker_create("KCF")
            # todo second time around it doesn't recreate tracker with new algorithm. I think it needs to be destroyed

            # initialize tracker bounding box
            bbox = (int(x), int(y), int(w), int(h))

            ok = tracker.init(frame, bbox)

            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 0, 255))

            while video_capture.isOpened():
                ret, frame = video_capture.read()
                if not ret:
                    break

                ok, bbox = tracker.update(frame)
                if ok:
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(frame, p1, p2, (0, 0, 255))

                frame_resized = cv2.resize(frame, (screen_width, screen_height))
                cv2.imshow('frame', frame_resized)

                if cv2.waitKey(1) == ord('q'):
                    break
                elif cv2.waitKey(1) == ord('p'):
                    print("Frame: " + str(video_capture.get(cv2.CAP_PROP_POS_FRAMES)))
                    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    plt.show()
        else:
            print("invalid choice")
        cv2.destroyAllWindows()

    video_capture.release()
