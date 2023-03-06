import cv2
from djitellopy import Tello


def stream_tello(Drone):
    Drone.connect()
    Drone.streamon()
    while True:
        img = Drone.get_frame_read().frame
        img = cv2.resize(img,(360,240))
        cv2.imshow("Image",img)
        cv2.waitKey(1)
