import cv2
import numpy as np
import argparse
import imutils
from datetime import datetime
kernel = np.ones((15,15),np.uint8) #tạo mặt nạ
# giải thuât Background subtraction để chuyển sang ảnh nhị phân
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()
if args.algo == 'MOG2':
    backSub = cv2.createBackgroundSubtractorMOG2()
else:
    backSub = cv2.createBackgroundSubtractorKNN()
capture = cv2.VideoCapture("11.mp4")
if not capture.isOpened():
    print('Unable to open: ' + args.input)
    exit(0)
#nếu bạn muốn nhận diện qua webcam thì đổi phần default thành true
parser.add_argument('--webcam', help="True/False", default=False)
#còn nếu bạn muốn nhận diện qua video thì đổi phần default dưới đây thành true
#hiện tại thì mình đã đổi sẵn phần default thành true nên nếu bạn chạy phần mềm
#nó sẽ nhận diện qua video
parser.add_argument('--play_video', help="True/False", default=True)
#đường dẫn tới file video
parser.add_argument('--video_path', help="Video Path", default="videos\Video.mp4")
args = parser.parse_args()
# lay du lieu file yolo
def load_yolo():
    yolov3weightspath = "yolov3\yolov3.weights"
    yolov3configpath = "yolov3\yolov3.cfg"
    coconamespath = "yolov3\coco.names"
    net = cv2.dnn.readNet(yolov3weightspath, yolov3configpath)
    classes = []
    with open(coconamespath, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return net, classes, output_layers
def detect_objects(frame, net, outputLayers):
    blob = cv2.dnn.blobFromImage(frame, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(outputLayers)
    return blob, outputs
def social_distance_detection(cap):
    model, classes, output_layers = load_yolo()
    writer = None
    #xử lý video
    while True:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=700)
        themvid = backSub.apply(frame)
        b=cv2.morphologyEx(themvid,cv2.MORPH_OPEN,kernel)# imopen
        a = cv2.morphologyEx(b, cv2.MORPH_CLOSE, kernel) # imclose
        height, width, channels = frame.shape
        blob, outputs = detect_objects(frame, model, output_layers)
        # khai báo 4 list
        boxes = [] #hộp giới hạn bao quanh vật thể
        centerPoints = [] #điểm trung tâm của người(để tinhc kc)
        confs = [] #chỉa số xac sauết của vạt thể  ,nếu nhỏ 0.5 ko xác định đc
        class_ids = []#chỉ số của vật thể (ví dụ chỉ số vật thể con người là 0, chỉ số vật thể xe đạp là 1,…)
        for output in outputs: # duyệt qua mỗi layer trong biến outputs mà ta đã xác định
            for detect in output:# bắt đầu duyệt và phát hiện trong layỷe
                scores = detect[5:]
                class_id = np.argmax(scores)
                conf = scores[class_id]
                if conf > 0.5 and class_id == 0:# lơn 0.5 thoa 0 là con người
                    #xác định tọa độ x,y
                    center_x = int(detect[0] * width)# cập nhật tọa độ điểm trung tâm x
                    center_y = int(detect[1] * height)# cập nhật tọa độ điểm trung tâm x
                   #xác định w h x y để vẽ các hinh chữ nhật
                    w = int(detect[2] * width)
                    h = int(detect[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    centerPoints.append((center_x, center_y))
                    confs.append(float(conf))
                    class_ids.append(class_id)
        indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                # bắt đầu vẽ khung hình chữ nhât và ghi chữ person
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 4)
                cv2.putText(frame, label, (x, y ), font, 1, (255,0,0), 2)
                cv2.rectangle(a, (x, y), (x + w, y + h),(255,255,255) , 2)
                cv2.putText(a, label, (x, y+15 ), font, 1,(255,255,255) , 2)
        # hien thi khung hinh
        cv2.imshow("Hồ Minh Đức", frame)
        cv2.imshow("hí hí hí",a)
        key = cv2.waitKey(1)
        # tat khung hinh
        if cv2.getWindowProperty("Hồ Minh Đức", 1) < 0:
            break
        # xuat file video
        if writer is None:
            date_time = datetime.now().strftime("%m-%d-%Y %H-%M-%S")
            OUTPUT_PATH = 'output\output {}.avi'.format(date_time)
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, 30, (frame.shape[1], frame.shape[0]), True)
        writer.write(frame)
    cap.release()
    writer.release()
def webcam_detect():
    cap = cv2.VideoCapture(0)
    social_distance_detection(cap)
def start_video(video_path):
    cap = cv2.VideoCapture(video_path)
    social_distance_detection(cap)
if __name__ == '__main__':
    webcam = args.webcam
    video_play = args.play_video
    if webcam:
        webcam_detect()
    if video_play:
        video_path = args.video_path
        start_video("11.mp4")
    cv2.destroyAllWindows()