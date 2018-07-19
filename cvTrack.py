import cv2
import sys
import json
from coordRetrv import *
import cv2

def main():
    # Set up tracker.
    # Instead of MIL, you can also use

    with open("config.json", "r") as read_file:
        config = json.load(read_file)

    cap = cv2.VideoCapture(config['image_location'])

    results = {}
    while(len(results) == 0):
        ret, frame = cap.read()
        if ret == True:
            results = coordRetrv(config['conf'], config['runtime'], frame)
        else:
            break

    print(len(results))
    tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE']
    tracker_type = tracker_types[2]

    tracker = cv2.TrackerKCF_create()

    # Other Types of tracking algorithms
    # tracker = cv2.TrackerBoosting_create()
    # tracker = cv2.TrackerMIL_create()
    # tracker = cv2.TrackerTLD_create()
    # tracker = cv2.TrackerMedianFlow_create()
    # tracker = cv2.TrackerGOTURN_create()
    # tracker = cv2.TrackerMOSSE_create()


    # Read video
    video = cv2.VideoCapture(config['image_location'])

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()

    for plate in results:
        coordinates = plate['coordinates']
        a = coordinates[0]
        b = coordinates[2]
        x1 = a['x']
        x2 = b['x']
        y1 = a['y']
        y2 = b['y']

    # Define an initial bounding box
    bbox = (x1, y1, (x2-x1), (y2-y1))


    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    i = 0
    while True:

        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            i += 1
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            print("Number of frames: " + str(i))


        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

main()