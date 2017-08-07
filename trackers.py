import cv2
from matplotlib import pyplot as plt

if __name__ == "__main__":

    # create tracker
    tracker = cv2.Tracker_create("MIL")

    # open video
    video_capture = cv2.VideoCapture("person_drone_video.avi")

    # initialize tracker bounding box
    bbox = (708, 444, 7, 7)
    ret, frame = video_capture.read()
    ok = tracker.init(frame, bbox)

    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    plt.show()

    while video_capture.isOpened():
        ret, frame = video_capture.read()

        if not ret:
            break

        ok, bbox = tracker.update(frame)

        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 0, 255))

        cv2.imshow("tracking", frame)

        if cv2.waitKey(1) == ord('q'):
            break
