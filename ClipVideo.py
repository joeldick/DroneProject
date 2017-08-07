import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

if __name__ == "__main__":
    video_capture = cv2.VideoCapture('drone_video.avi')
    # video_capture = cv2.VideoCapture('short_drone_video.avi')

    # get information about video
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print("frames per second: " + str(int(fps)))

    num_frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    print("number of frames: " + str(int(num_frames)))

    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # create video output
    fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')
    video_output = cv2.VideoWriter('person_drone_video.avi', fourcc, fps, (width, height))

    frameCounter = 0

    while video_capture.isOpened():
        # grabs and retrieves the next frame
        (ret, frame) = video_capture.read()
        if ret:
            # clip the drone video from start_time seconds to end_time seconds
            # only needed to do this once
            start_time = 31
            end_time = 80
            if (frameCounter > start_time * 30 and frameCounter < end_time * 30):
                print("saving frame: " + str(frameCounter))
                video_output.write(frame)
            frameCounter += 1
            if frameCounter >= end_time * 30:
                break
                # cv2.imshow('frame', frame)
                # if cv2.waitKey(int(1000/fps)) == ord('q') or cv2.getWindowProperty('frame', 0):
                #    break

    print("number of frames played: " + str(frameCounter))
    video_length = frameCounter / fps
    print("length: " + str(video_length) + " seconds")
    video_capture.release()
    video_output.release()
    cv2.destroyAllWindows()
