import cv2
import time
import numpy as np
from robomaster import robot
from cvzone.HandTrackingModule import HandDetector
import math

from imageai.Detection import ObjectDetection
import os


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
            # print('line_type', line_type)
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


def take_photo(num, img, name):
    img_path = "C:\\Users\\satori\\Desktop\\picture\\"
    cv2.imwrite(img_path + str(num) + ".png", img)

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path, "./yolov3.pt"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(
        input_image=os.path.join(execution_path, img_path + str(num) + ".png"),
        output_image_path=os.path.join(execution_path, img_path + str(num) + "new.png"),
        minimum_percentage_probability=30)
    for eachObject in detections:
        name.append(eachObject["name"])
    num = num + 1
    return num, name


if __name__ == '__main__':

    photo_num = 0
    book_label = []
    label = []
    distance = []

    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    # ep_robot.initialize(conn_type="sta", sn="3JKCHCH00104MN")

    ep_camera = ep_robot.camera
    ep_sensor = ep_robot.sensor

    ep_sensor.sub_distance(freq=5, callback=distance)
    dist = distance[0]

    ep_camera.start_video_stream(display=True)
    time.sleep(2)
    img = ep_camera.read_cv2_image(strategy="newest")
    time.sleep(2)


    photo_num, book_label = take_photo(photo_num, img, book_label)

    for i in range(0, len(book_label)):
        print(str(i) + ':' + book_label[i])
    index = input("选择标签主体内容")

    book = book_label[int(index)]

    distance_cm = 10000  # 初始化距离变量

    # cap = cv2.VideoCapture(0)  # 打开摄像头
    detector = HandDetector(detectionCon=0.8, maxHands=2)  # 创建手部检测器对象

    focalLength = 875  # 焦距（根据摄像头和实际设置调整）
    # success, imga = cap.read()  # 读取摄像头图像

    ep_vision = ep_robot.vision
    # ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis
    ep_robot.set_robot_mode(mode="chassis_lead")
    car_speed = 0.2

    # ep_camera.start_video_stream(display=False)
    result = ep_vision.sub_detect_info(name="line", color="blue", callback=on_detect_thing)

    time.sleep(1)
    run = False

    while True:
        img = ep_camera.read_cv2_image(strategy="newest")



        hands, img = detector.findHands(img)  # 检测手部

        if hands:
            hand1 = hands[0]  # 获取第一只手
            lmList = hand1["lmList"]  # 获取手部关键点坐标列表
            if len(lmList) >= 4:  # 确保至少检测到了食指和拇指的关键点
                x1, y1 = lmList[4][1], lmList[4][2]  # 食指指尖的坐标
                x2, y2 = lmList[8][1], lmList[8][2]  # 拇指指尖的坐标
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # 计算食指和拇指指尖的中心坐标
                dis = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # 计算手指间的距离
                # 将像素距离转换为厘米
                distance_cm = (focalLength * 2.54) / dis
                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)  # 绘制食指指尖圆圈
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)  # 绘制拇指指尖圆圈
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)  # 绘制食指和拇指间的连线
                cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)  # 绘制手指中心点圆圈

        cv2.putText(img, f"Distance: {int(distance_cm)} cm", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255),
                    2)  # 显示手指间的距离
        print(f"Distance: {int(distance_cm)} cm")  # 打印距离

        l = len(line)
        line_tmp = line.copy()
        print(distance_cm)
        if (len(line_tmp) > 0) & run & (distance_cm >= 20):
            print("Follow line")
            for j in range(0, len(line_tmp)):
                cv2.circle(img, line_tmp[j].pt, 3, line_tmp[j].color, -1)
            point_x_3 = line_tmp[4]._x
            error_3 = point_x_3 - 0.5
            angle_output = 190 * error_3
            print("Angle_Out", angle_output)

            point_x_8 = line_tmp[8]._x
            error_8 = 0.5 - point_x_8
            speed_output = 0.85 - 0.6 * abs(error_8)
            print("speed_output", speed_output)

            ep_chassis.drive_speed(x=car_speed, y=0, z=1.5 * angle_output)
        elif (distance_cm < 20):
            print("距离很短 要停下来")
            ep_chassis.move(x=0, y=0, z=0).wait_for_completed()
            if key == ord('f'):
                break
            photo_num, label = take_photo(photo_num, img, label)
            distance_cm = 10000

            for i in range(0, len(label)):
                if book == label[i]:
                    run = False
                    print("confirm")
                    break


        else:
            print("No line, rfl = ", run)
            ep_chassis.move(x=0, y=0, z=0).wait_for_completed()

        cv2.imshow("Line", img)

        key = cv2.waitKey(1)
        if key == ord('w'):
            ep_chassis.drive_speed(x=car_speed, y=0, z=0)
        if key == ord('v'):
            ep_chassis.move(x=0, y=0, z=0).wait_for_completed()
            run = False
        if key == ord('n'):
            run = True
        if key == ord('g'):
            break

    result = ep_vision.unsub_detect_info(name="line")
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()
    ep_robot.close()
