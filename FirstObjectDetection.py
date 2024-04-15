from imageai.Detection import ObjectDetection
import os

name = []
execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "yolov3.pt"))
detector.loadModel()
detections = detector.detectObjectsFromImage(
    input_image=os.path.join(execution_path, "C:\\Users\\satori\\PycharmProjects\\ImageAI\\test-images\\2.jpg"),
    output_image_path=os.path.join(execution_path,
                                   "C:\\Users\\satori\\PycharmProjects\\ImageAI\\test-images\\2new.jpg"),
    minimum_percentage_probability=30)

for eachObject in detections:
    # print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
    # print("--------------------------------")
    name.append(eachObject["name"])

j = len(name)
for i in range(0, j):
    print(str(i) + ':' + name[i])

index = input("xxx")

num = name[int(index)]
print(num)
