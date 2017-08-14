import cv2
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':

    # ask user to choose file
    filename = 'drone_video_2.mp4'
    video_capture = cv2.VideoCapture(filename)

    while True:
        # ask user for which frame to start from
        start_frame = 0

        # read first frame
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, int(start_frame))
        ret, frame = video_capture.read()

        if not ret:
            print("Not able to read file.")
            continue

        kernel = 5
        #blur = cv2.blur(frame, (kernel, kernel))
        blur = cv2.GaussianBlur(frame, (kernel, kernel), 0)
        #blur = cv2.medianBlur(frame, kernel)
        #blur = cv2.bilateralFilter(frame, 9, 75, 75)

        low = int(input("low: "))
        high = int(input("high: "))
        edges = cv2.Canny(frame,low,high)

        plt.subplot(2, 2, 1)
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.title('Original')
        #plt.xticks([]), plt.yticks([])
        plt.subplot(2, 2, 3)
        plt.imshow(cv2.cvtColor(blur, cv2.COLOR_BGR2RGB), cmap='gray')
        plt.title('Blur')
        plt.subplot(2, 2, 4)
        plt.imshow(edges, cmap='gray')
        plt.title('Edges')
        #plt.xticks([]), plt.yticks([])
        plt.show()

    video_capture.release()
