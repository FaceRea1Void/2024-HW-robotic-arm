import os
import cv2
import time
import numpy as np
from robomaster import robot
from imageai.Detection import ObjectDetection


def process(image):
    # RGB转HSV色彩空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 识别红色
    low_hsv = np.array([0, 43, 46])
    high_hsv = np.array([5, 255, 255])

    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)  # 取值函数

    dst = cv2.blur(mask, (1, 16))  # 均值模糊 : 去掉提取完颜色的随机噪声图片

    circles = cv2.HoughCircles(dst, cv2.HOUGH_GRADIENT, 1, 40, param1=100, param2=60, minRadius=80, maxRadius=150)
    # 霍夫圆检测函数，其中的参数需要根据情况修改

    pos = [0, 0]
    if circles is not None:
        for i in circles[0, :]:
            print("draw circles")
            cv2.circle(image, (int(i[0]), int(i[1])), int(i[2]), (0, 0, 255), 4)  # 画圆
            cv2.circle(image, (int(i[0]), int(i[1])), 2, (0, 0, 255), 3)  # 画圆心

            pos[0] = i[0]
            pos[1] = i[1]
            ret = True
    else:
        print('未识别到圆形图案, no circles')
        ret = False
    return image, pos, ret


def out_limit(value, maxout, minout):  # 限值函数，限值角速度
    if (value > maxout):
        value = maxout
    elif (value < minout):
        value = minout
    return value


class PointInfo:

    def __init__(self, x, y, theta, c):
        self._x = x
        self._y = y
        self._theta = theta
        self._c = c

    @property
    def pt(self):
        return int(self._x * 1280), int(self._y * 720)

    @property
    def color(self):
        return 255, 255, 255


line = []
line_counter = 10


def on_detect_thing(thing_info):
    global line_counter
    number = len(thing_info)
    if number > 0:
        if number >= 10:  # if len(thing_info[1] == 4)
            line.clear()
            line_counter = 10
            line_type = thing_info[0]
            for i in range(1, number):
                x, y, ceta, c = thing_info[i]
                line.append(PointInfo(x, y, ceta, c))
    else:
        line_counter -= 1
        if line_counter < 0:
            line_counter = 10
            line.clear()
        print('未识别到线 - not detected line')


execution_path = os.getcwd()


def take_photo(num, frame, name):
    cv2.imwrite("C:\\Users\\satori\\Desktop\\" + "Photo" + str(num) + ".png", frame)
    num = num + 1

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path, "yolov3.pt"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, "image2.jpg"),
                                                 output_image_path=os.path.join(execution_path, "image2new.jpg"),
                                                 minimum_percentage_probability=30)
    i = 0
    for eachObject in detections:
        name[0] = eachObject["name"]
        i = i + 1
    return num,


if __name__ == '__main__':

    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis
    ep_robot.set_robot_mode(mode="chassis_lead")

    car_speed = 0.2
    run = False
    photoNum = 0

    ep_camera.start_video_stream(display=False)
    result = ep_vision.sub_detect_info(name="line", color="blue", callback=on_detect_thing)

    time.sleep(1)

    while True:
        img = ep_camera.read_cv2_image(strategy="newest")

        l = len(line)
        line_tmp = line.copy()

        if (len(line_tmp) > 0) & run:

            for j in range(0, len(line_tmp)):
                cv2.circle(img, line_tmp[j].pt, 3, line_tmp[j].color, -1)
            point_x_3 = line_tmp[4]._x
            error_3 = point_x_3 - 0.5
            angle_output = 190 * error_3

            point_x_8 = line_tmp[8]._x
            error_8 = 0.5 - point_x_8
            speed_output = 0.85 - 0.6 * abs(error_8)

            ep_chassis.drive_speed(x=car_speed, y=0, z=1.5 * angle_output)
        else:
            print("No line, rfl = ", run)
            ep_chassis.move(x=0, y=0, z=0).wait_for_completed()

        cv2.imshow("Line", img)

        key = cv2.waitKey(1)

        if key == ord('v'):
            ep_chassis.move(x=0, y=0, z=0).wait_for_completed()
            run = False
        if key == ord('n'):
            run = True
        if key == ord('p'):
            run = False
            photoNum = take_photo(photoNum, img)
        if key == ord('q'):
            break

    result = ep_vision.unsub_detect_info(name="line")
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()
