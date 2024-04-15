import os
import cv2
import time
import keyboard
from robomaster import robot
from imageai.Detection import ObjectDetection

distance = [10000]


def sub_data(sub_info):
    global distance
    distance = sub_info

    if distance[0] < 300:
        print("识别到障碍物")
        ep_chassis.move(x=0, y=0, z=0)
        ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)
    elif distance[0] > 600:
        print("障碍物移除")


def sub_pos(position_info):
    x, y, z = position_info
    print("chassis position: x:{0}, y:{1}, z:{2}".format(x, y, z))
    if -0.85 < x <= 0:
        ep_chassis.move(x=0.83, y=0, z=0, xy_speed=1.8).wait_for_completed()
    else:
        ep_chassis.drive_speed(x=0, y=0, z=0)
        ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)

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

    shelf = 0
    photo_num = 0
    label = []
    book_label = []

    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_camera = ep_robot.camera
    ep_sensor = ep_robot.sensor
    ep_chassis = ep_robot.chassis

    ep_camera.start_video_stream(display=True)
    img = ep_camera.read_cv2_image(strategy="newest")

    ep_robot.set_robot_mode(mode="chassis_lead")

    # photo_num, book_label = take_photo(photo_num, img, book_label)
    # for i in range(0, len(book_label)):
    #     print(str(i) + ':' + book_label[i])
    # index = input("选择标签主体内容")
    # book = book_label[int(index)]
    #
    # for i in range(0, len(label)):
    #     if book == label[i]:
    #         shelf = i

    # keyboard.wait('y')

    ep_sensor.sub_distance(freq=5, callback=sub_data)
    ep_chassis.sub_position(freq=10, callback=sub_pos)

    # ep_chassis.move(x=0.8, y=0, z=0, xy_speed=2).wait_for_completed()
    # ep_chassis.drive_wheels(w1=0, w2=0, w3=0, w4=0)

    # ep_chassis.drive_speed(x=0.5, y=0, z=0)
    time.sleep(50)


    ep_robot.close()
