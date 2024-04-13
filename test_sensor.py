import math
import time
import cv2
from robomaster import robot
from robomaster import vision

class MarkerInfo:

    def __init__(self, x, y, w, h, info):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._info = info

    @property
    def pt1(self):
        return int((self._x - self._w / 2) * 1280), int((self._y - self._h / 2) * 720)

    @property
    def pt2(self):
        return int((self._x + self._w / 2) * 1280), int((self._y + self._h / 2) * 720)

    @property
    def center(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def text(self):
        return self._info


markers = []
distance = []
dist_threshold = 600

def on_detect_marker(marker_info):
    number1 = len(marker_info)
    markers.clear()
    for i in range(0, number1):
        x, y, w, h, info = marker_info[i]
        markers.append(MarkerInfo(x, y, w, h, info))


def sub_data_handler(sub_info):
    global distance
    distance = sub_info


if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_robot.set_robot_mode("CHASSIS_LEAD")
    ep_sensor = ep_robot.sensor

    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis
    # ep_gimbal = ep_robot.gimbal
    ep_led = ep_robot.led

    #ep_led.set_led(comp="all", r=0,g=255,b=0,effect="on")
    ep_camera.start_video_stream(display=False)
    ep_sensor.sub_distance(freq=5, callback=sub_data_handler)
    step = 0

    time.sleep(3)

    while 1:
        img = ep_camera.read_cv2_image(strategy="newest", timeout=2)
        ep_led.set_led(comp="all", r=0, g=255, b=0, effect="on")
        dist_tmp = distance[0]
        print(dist_tmp)

        if (dist_tmp <= dist_threshold):
            # 检测到前方有障碍物，就先闪红灯，30s后还是有障碍物直接原地180度掉头
            ep_led.set_led(comp="all", r=255, g=0, b=0, effect="on")
            ep_chassis.move(x=0,y=0,z=0,xy_speed=0)
        # if dist_tmp >= dist_threshold and step == 0:
        #     ep_chassis.move(x=2,y=0,z=0,xy_speed=0.5).wait_for_completed()
        #     step += 1
        #     continue
        # if step == 1:
        #     ep_chassis.move(x=0,y=0,z=-90,z_speed=20).wait_for_completed()
        #     step += 1
        # if dist_tmp >= dist_threshold and step == 2:
        #     ep_chassis.move(x=1, y=0, z=0, xy_speed=0.5)

        cv2.imshow("Markers", img)
        key = cv2.waitKey(1)

        if key == 27:
            ep_sensor.unsub_distance()
            result = ep_vision.unsub_detect_info(name="marker")
            cv2.destroyAllWindows()
            ep_camera.stop_video_stream()
            ep_robot.close()
            break