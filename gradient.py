import cv2
import numpy as np
from matplotlib import pyplot as plt
from tkinter import Tk
from tkinter import filedialog

if __name__ == '__main__':

    # ask user to choose file
    Tk().withdraw()
    filename = filedialog.askopenfilename()
    video_capture = cv2.VideoCapture(filename)
    video_capture = cv2.VideoCapture(filename)

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

        # ask user to choose tracking algorithm
        algorithm = int(input("Select tracking method - SobelX(1), SobelY(2), Scharr(3), Laplacian (4), Canny(5): "))
        while True:
            if algorithm == 1:
                print("Chose SobelX")
                break
            elif algorithm == 2:
                print("Chose SobelY")
                break
            elif algorithm == 3:
                print("Chose Scharr")
                break
            elif algorithm == 4:
                print("Chose Laplacian")
                break
            elif algorithm == 5:
                print("Chose Canny")
                break
            else:
                print("Invalid selection")

        # ask user to choose kernel size
        if algorithm == 1 or algorithm == 2:
            try:
                kernel_size = int(input("Select kernel size (1, 3, 5, or 7): "))
            except:
                kernel_size = 1

        # read first frame
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, int(start_frame))
        ret, frame = video_capture.read()

        if not ret:
            print("Not able to read file.")
            continue

        if algorithm == 1:
            edges = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=kernel_size)
        elif algorithm == 2:
            edges = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=kernel_size)
        elif algorithm == 3:
            edges = cv2.Scharr(frame, cv2.CV_64F, 0, 1)
        elif algorithm == 4:
            edges = cv2.Laplacian(frame, cv2.CV_64F)
        elif algorithm == 5:
            low = int(input("low: "))
            high = int(input("high: "))
            edges = cv2.Canny(frame,low,high)
        else:
            print("invalid choice")
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.title('Original')
        #plt.xticks([]), plt.yticks([])
        plt.subplot(1, 2, 2)
        plt.imshow(edges, cmap='gray')
        plt.title('Edges')
        #plt.xticks([]), plt.yticks([])
        plt.show()

    video_capture.release()
