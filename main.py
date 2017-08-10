import cv2
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':

    while True:
        filename = input("Type filename, or 'q' for 'quit': ")

        if filename == 'q':
            break

        video_capture = cv2.VideoCapture(filename)

        # ask user for starting frame
        num_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if num_frames is 0:
            print("Video has no frames.")
            break
        try:
            start_frame = int(input("Type starting frame [0 - " + str(num_frames - 1) + "]: "))
        except:
            start_frame = 0

        # read first frame
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, int(start_frame))
        (ret, frame) = video_capture.read()

        if not ret:
            print("Not able to read file.")
            continue

        # ask user to select object to track
        print("Select object to track")
        x, y, w, h = cv2.selectROI(frame, False)
        cv2.destroyAllWindows()

        # ask user to choose tracking algorithm
        algorithm = int(input("Select tracking method - Meanshift(1), Camshift(2), MIL(3), KCF(4): "))
        if algorithm == 1:
            print("meanshift")
        elif algorithm == 2:
            print("camshift")
        elif algorithm == 3:
            print("MIL")
        elif algorithm == 4:
            print("KCF")
        else:
            print("Invalid selection")
            break

        if algorithm == 1 or algorithm == 2:
            print("Meanshift/Camshift...")

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
                cv2.imshow('frame', frame)

                if cv2.waitKey(1) == ord('q'):
                    break

        elif algorithm == 3 or algorithm == 4:
            # create tracker
            if algorithm == 3:
                tracker = cv2.Tracker_create("MIL")
            elif algorithm == 4:
                tracker = cv2.Tracker_create("KCF")
            # todo second time around it doesn't recreate tracker with new algorithm. I think it needs to be destroyed

            # initialize tracker bounding box
            # person in person_drone_video.avi
            # bbox = (708, 444, 7, 7)
            # golf ball in drone_video.avi
            bbox = (int(x), int(y), int(w), int(h))

            ok = tracker.init(frame, bbox)

            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 0, 255))
            # plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            # plt.show()

            while video_capture.isOpened():
                ret, frame = video_capture.read()
                if not ret:
                    break

                ok, bbox = tracker.update(frame)
                if ok:
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(frame, p1, p2, (0, 0, 255))

                cv2.imshow('frame', frame)

                if cv2.waitKey(1) == ord('q'):
                    break
        else:
            print("invalid choice")

        cv2.destroyAllWindows()
        video_capture.release()
