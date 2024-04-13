import cv2
import numpy as np
import robomaster
from robomaster import robot
import time
from pymycobot import MyCobotSocket

ID = {'1', '2', '3', '4', '5'}
markers = []
markers_info = []
distance = []
dist_threshold = 1000

mc = MyCobotSocket("192.168.43.38", 9000)

# 树莓派版本需要输入connect函数，默认值为("/dev/ttyAMA0","1000000")
mc.connect("/dev/ttyAMA0", "1000000")

def grab02shelf():
    # 初态
    mc.send_angles([0, 0, 0, 0, 0, 0], 30)
    # 回到夹书准备状态（收缩）
    mc.send_angles([0, -15, 10, 0, 92.1, 0], 30)
    time.sleep(2)
    # 回到夹书准备状态（转向）
    mc.send_angles([104.15, -15, 10, 3.9, 92.1, 16.8], 30)
    time.sleep(2)
    # 夹爪往里伸
    # mc.send_angles([104.15, 50, -59.8, -7.23, 80, 7.2], 20)
    # mc.send_angles([104.15, 60.7, -59.8, -7.23, 90.8, 7.2], 20)
    # mc.send_angles([106, 60.7, -59.8, -7.23, 78, 9], 30)
    mc.send_angles([106, 52, -60, -7.23, 82, 9], 30)
    time.sleep(2)
    # 夹紧书本
    mc.set_gripper_value(50, 40)
    time.sleep(3)
    # 拿起书本
    # mc.send_angles([104.8, -10, -65, 3.9, 68, 16.8], 20)
    mc.send_angles([106, -10, -60, 3.9, 68, 16.8], 20)
    time.sleep(2)


def grab01shelf():
    # 回到夹书准备状态（收缩）
    mc.send_angles([0, -15, 10, 0, 92.1, 0], 30)
    time.sleep(1)
    # 回到夹书准备状态（转向）
    mc.send_angles([122.7, -15, 10, 3.9, 92.1, 16.8], 30)
    time.sleep(2)
    # 夹爪往里伸
    mc.send_angles([122.7, 70, -87, 7, 119, 35], 30)
    time.sleep(2)
    # 调整位置
    mc.send_angles([122.7, 70, -90, 0, 88.6, 35], 40)
    time.sleep(2)
    # 夹紧书本
    mc.set_gripper_value(50, 40)
    time.sleep(3)
    # 拿起书本
    mc.send_angles([122.7, -10, -90, 0, 88.6, 25.6], 20)
    time.sleep(3)


def grab03shelf():
    # 回到夹书准备状态（收缩）
    mc.send_angles([0, -15, 10, 0, 92.1, 0], 30)
    time.sleep(2)
    # 回到夹书准备状态（转向）
    mc.send_angles([84.11, -15, 10, 3.9, 92.1, 16.8], 30)
    time.sleep(2)
    # 夹爪往里伸
    mc.send_angles([84.11, 42.71, -43.9, -0.5, 78, -9], 30)
    time.sleep(2)
    # 夹紧书本
    mc.set_gripper_value(50, 40)
    time.sleep(3)
    # 拿起书本
    mc.send_angles([84.11, -20, -43.9, -0.5, 65, -6], 20)
    time.sleep(2)


def grab04shelf():
    # 回到夹书准备状态（收缩）
    mc.send_angles([0, -15, 10, 0, 92.1, 0], 30)
    time.sleep(2)
    # 回到夹书准备状态（转向）
    mc.send_angles([66.44, -15, 10, 3.9, 92.1, 16.8], 30)
    time.sleep(2)
    # 夹爪往里伸
    mc.send_angles([66.44, 50.71, -51.2, 1.3, 65, -18.4], 30)
    time.sleep(2)
    # 夹紧书本
    mc.set_gripper_value(50, 40)
    time.sleep(3)
    # 拿起书本
    mc.send_angles([66.44, -10, -51.2, 1.3, 68, -18.4], 20)
    time.sleep(2)


def placebook1():
    # 转向书架并将夹爪转正
    mc.send_angles([45, -20, -43.9, -0.5, 65, -6], 30)
    time.sleep(3)
    # 转进去
    mc.send_angles([45, -20, -10, -0.5, 100, -6], 30)
    time.sleep(2)
    mc.send_angles([0, -20, -10, -0.5, 100, -6], 30)
    time.sleep(2)
    # 往下放 （原来2 53； 5 70）
    mc.send_angles([0, 60, -65, 0, 50, 0], 30)
    time.sleep(2)
    # 伸进去书架
    # 还没写dd
    # 松开夹爪
    mc.set_gripper_value(100, 70)
    time.sleep(2)
    # 从书架收回来
    # 还没写dd
    # 回到夹书准备状态
    mc.send_angles([0, -15, 10, 0, 92.1, 0], 20)


def placebook2():
    # 转向书架并将夹爪转正
    mc.send_angles([45, -20, -43.9, -0.5, 65, -6], 30)
    time.sleep(3)
    # 转进去
    mc.send_angles([45, -20, -10, -0.5, 100, -6], 30)
    time.sleep(2)
    # 放书
    mc.send_angles([25, -20, -10, -0.5, 100, -6], 30)
    time.sleep(2)
    mc.send_angles([25, 10, -10, -0.5, 60, -6], 30)
    time.sleep(2)
    mc.send_angles([25, 46, -4, -0.5, 6, 5], 30)
    time.sleep(2)
    # 伸进去书架
    # 还没写dd
    mc.send_angles([12, 46, -4, -0.5, 6, 5], 20)
    time.sleep(2)
    # 松开夹爪
    mc.set_gripper_value(100, 70)
    time.sleep(2)
    # 从书架收回来
    # 还没写dd
    # 回到夹书准备状态
    mc.send_angles([0, -15, 10, 0, 92.1, 0], 20)


def placebook3():
    # 转向书架并将夹爪转正
    mc.send_angles([45, -20, -43.9, -0.5, 65, -6], 30)
    time.sleep(3)
    # 转进去
    mc.send_angles([45, -20, -10, -0.5, 100, -6], 30)
    time.sleep(2)
    # 放书
    mc.send_angles([45, 30, -10, -0.5, 30, 22], 30)
    time.sleep(2)
    mc.send_angles([45, 50, -25, -0.5, 8, 22], 30)
    time.sleep(2)
    mc.send_angles([30, 50, -25, -0.5, 8, 22], 30)
    time.sleep(2)
    mc.send_angles([27, 50, -20, -9, 8, 22], 30)
    time.sleep(2)
    # 松爪
    mc.set_gripper_value(100, 70)
    time.sleep(4)
    # 抽出爪子
    mc.send_angles([27, 50, -20, -9, 50, 22], 20)
    time.sleep(2)
    # 回到夹书准备状态
    mc.send_angles([0, -15, 10, 0, 92.1, 0], 20)


def placebook4():
    # 转向书架并将夹爪转正
    mc.send_angles([45, -20, -43.9, -0.5, 65, -6], 30)
    time.sleep(3)
    # 转进去
    mc.send_angles([45, -20, -10, -0.5, 100, -6], 30)
    time.sleep(2)
    # 4 放书
    mc.send_angles([45, 30, -10, -0.5, 30, 22], 30)
    time.sleep(2)
    mc.send_angles([45, 55, -20, -0.5, 7, 22], 30)
    time.sleep(2)
    mc.send_angles([33, 60, -20, -8, -5, 15], 30)
    time.sleep(2)
    # 松爪
    mc.set_gripper_value(100, 70)
    time.sleep(4)
    # 抽出爪子
    mc.send_angles([33, 60, -20, -8, 30, 25], 20)
    time.sleep(2)
    # 回到夹书准备状态
    mc.send_angles([0, -15, 10, 0, 92.1, 0], 20)


def grabbookN(a):
    # 回归初态
    mc.send_angles([0, 0, 0, 0, 0, 0], 20)
    mc.send_angles([0, -15, 10, 0, 92.1, 0], 20)
    mc.set_gripper_value(100, 40)
    # 选择车上的书架
    if a == 1:
        grab01shelf()
        placebook1()
    if a == 2:
        grab02shelf()
        placebook2()
    if a == 3:
        grab03shelf()
        placebook3()
    if a == 4:
        grab04shelf()
        placebook4()

def move_1():
    print("执行在1号书架放书的动作")
    ep_chassis.move(x=1.2,y=0,z=0,xy_speed=0.8).wait_for_completed()
    grabbookN(1)
    grabbookN(2)
    grabbookN(3)
    grabbookN(4)
    ep_chassis.move(x=-1.2,y=0,z=0,xy_speed=1.5)
def move_2():
    print("执行在2号书架放书的动作")
    ep_chassis.move(x=2.25, y=0, z=0, xy_speed=0.8).wait_for_completed()
    ep_chassis.move(x=0, y=0, z=90, z_speed=30).wait_for_completed()
    ep_chassis.move(x=0.9, y=0, z=0, xy_speed=0.8).wait_for_completed()
    grabbookN(1)
    grabbookN(2)
    grabbookN(3)
    grabbookN(4)
    ep_chassis.move(x=-1.0, y=0, z=0, xy_speed=1.5).wait_for_completed()
    # ep_chassis.move(x=0, y=0, z=90, z_speed=30).wait_for_completed()
    ep_chassis.move(x=0, y=-2.25, z=0, xy_speed=1.5)
def move_3():
    print("执行在3号书架放书的动作")
    ep_chassis.move(x=2.25, y=0, z=0, xy_speed=0.8).wait_for_completed()
    ep_chassis.move(x=0, y=0, z=90, z_speed=30).wait_for_completed()
    ep_chassis.move(x=1.8, y=0, z=0, xy_speed=0.8).wait_for_completed()
    ep_chassis.move(x=0, y=0, z=-90, z_speed=30).wait_for_completed()
    ep_chassis.move(x=1, y=0, z=0, xy_speed=0.8).wait_for_completed()
    grabbookN(1)
    grabbookN(2)
    grabbookN(3)
    grabbookN(4)
    ep_chassis.move(x=0, y=2.0, z=0, xy_speed=1.5).wait_for_completed()
    # ep_chassis.move(x=0, y=0, z=-180, z_speed=30).wait_for_completed()
    ep_chassis.move(x=-3.25, y=0, z=0, xy_speed=1.5)
def move_4():
    print("执行在4号书架放书的动作")
    ep_chassis.move(x=2.25, y=0, z=0, xy_speed=0.8).wait_for_completed()
    ep_chassis.move(x=0, y=0, z=90, z_speed=20).wait_for_completed()
    ep_chassis.move(x=1.8, y=0, z=0, xy_speed=0.8).wait_for_completed()
    ep_chassis.move(x=0, y=0, z=-90, z_speed=20).wait_for_completed()
    ep_chassis.move(x=1.78, y=0, z=0, xy_speed=0.8).wait_for_completed()
    ep_chassis.move(x=0, y=0, z=-90, z_speed=20).wait_for_completed()
    ep_chassis.move(x=0.8, y=0, z=0, xy_speed=0.8).wait_for_completed()
    # grabbookN(1)
    # grabbookN(2)
    # grabbookN(3)
    # grabbookN(4)
    ep_chassis.move(x=1.2, y=0, z=0, xy_speed=1.5).wait_for_completed()
    # ep_chassis.move(x=0, y=0, z=-90, z_speed=30).wait_for_completed()
    ep_chassis.move(x=0, y=1.5, z=0, xy_speed=1.5).wait_for_completed()
    time.sleep(5)
    ep_chassis.move(x=0, y=2.5, z=0, xy_speed=1.5)

# 返回为图标的中心坐标(x, y)，物体的weight和height，以及信息
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


def on_detect_thing(thing_info):  # if detect something
    # 识别到的物体用数组来存储，如果这个数组长度大于0，就说明找到了物体
    obj_num = len(thing_info)

    if obj_num > 0:
        print("find a object")

        if thing_info[0] is None:
            print("Thing is empty")
        if thing_info[0] == 0:
            print("Thing is zero")

        else:
            number = len(thing_info)
            print("Item count", number)
            # print("Markers cleared")
            markers.clear()  # Clear the original data in the list
            for i in range(0, number):  # Get information about the current marker
                x, y, w, h, info = thing_info[i]
                if(info not in markers_info):
                    markers_info.append(info)
                markers.append(MarkerInfo(x, y, w, h, info))
                print("markers_info is :",markers_info)

    else:
        # 啥都没找到
        markers.clear()
        markers_info.clear()
        print('nothing detected')

def sub_data_handler(sub_info):
    global distance
    distance = sub_info

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type='sta',sn='3JKCHC60010396')

    ep_vision = ep_robot.vision
    # ep_gimbal = ep_robot.gimbal
    ep_robot.set_robot_mode(mode="CHASSIS_LEAD")
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis
    ep_sensor = ep_robot.sensor
    ep_led = ep_robot.led
    # robot_speed = 0.3
    ep_camera.start_video_stream(display=False)

    result1 = ep_vision.sub_detect_info(name="marker", callback=on_detect_thing)
    result2 = ep_sensor.sub_distance(freq=5, callback=sub_data_handler)

    time.sleep(1)

    start_point = True  #代表是否在起点
    cnt1 = 0
    cnt2 = 0
    cnt3 = 0
    cnt4 = 0
    step = 0
    while True:
        img = ep_camera.read_cv2_image(strategy="newest")
        dist_tmp = distance[0]

        # if dist_tmp <= dist_threshold:
        #     print("有障碍物")

        if start_point and len(markers_info) == 0:
            #  这说明在起点，啥也没有找到
            # ep_chassis.drive_speed(x=0.0, y=0.0, z=0.0)
            print("目前在起点")
        elif markers_info == ['1']:
            if cnt1 == 0:
                start_point = False
                cnt1 += 1
                move_1()
                # if dist_tmp >= dist_threshold and step == 0:
                #     ep_chassis.move(x=1.2, y=0, z=0, xy_speed=0.5).wait_for_completed()
                #     step += 1
                # if step == 1:
                #     ep_chassis.move(x=0, y=0, z=90, z_speed=20).wait_for_completed()
                #     step += 1
                # if dist_tmp >= dist_threshold and step == 2:
                #     ep_chassis.move(x=1, y=0, z=0, xy_speed=0.5)
                start_point = True
            else:
                print("第一个书架满了")
        elif markers_info == ['2']:
            if cnt2 == 0:
                start_point = False
                cnt2 += 1
                move_2()
                start_point = True
            else:
                print("第二个书架满了")
        elif markers_info == ['3']:
            if cnt3 == 0:
                start_point = False
                cnt3 += 1
                move_3()
                start_point = True
            else:
                print("第三个书架满了")
        elif markers_info == ['4']:
            if cnt4 == 0:
                start_point = False
                cnt4 += 1
                move_4()
                start_point = True
            else:
                print("第四个书架满了")
        step = 0
        cv2.imshow("IMG", img)

        key = cv2.waitKey(1)

        if key == 27:
            result = ep_vision.unsub_detect_info(name="line")
            cv2.destroyAllWindows()
            ep_camera.stop_video_stream()
            ep_robot.close()
            break



