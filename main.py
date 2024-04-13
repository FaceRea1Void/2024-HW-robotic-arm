from pymycobot import MyCobotSocket
import time

# 默认使用9000端口
# 其中"192.168.11.15"为机械臂IP，请自行输入你的机械臂IP
# 192.168.43.38 // 8888手机热点局域网
# 10.42.0.1 // 大象自己的局域网
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
    mc.set_gripper_value(0, 40)
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
    mc.set_gripper_value(0, 40)
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
    mc.set_gripper_value(0, 40)
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
    mc.set_gripper_value(0, 40)
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
    mc.set_gripper_value(100, 60)
    time.sleep(2)
    # 抽出爪子
    mc.send_angles([27, 50, -20, -9, 50, 22], 20)
    time.sleep(3)
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
    mc.set_gripper_value(100, 60)
    time.sleep(2)
    # 抽出爪子
    mc.send_angles([33, 60, -20, -8, 30, 25], 20)
    time.sleep(3)
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


if __name__ == "__main__":
    mc.send_angles([0, 0, 0, 0, 0, 0], 20)
    mc.send_angles([0, -15, 10, 0, 92.1, 0], 20)
    mc.set_gripper_value(100, 40)
    # grabbookN(1)
    # grabbookN(2)
    # grabbookN(3)
    # grabbookN(4)


























