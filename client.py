import cv2
import io
import socket
import struct
import time
import pickle
import zlib

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.131', 8000))
connection = client_socket.makefile('wb')

gstreamer_pipeline  = "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)1920, height=(int)1080, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"#2Mpx
# gstreamer_pipeline  = "nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)4032, height=(int)3040, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)4032, height=(int)3040, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"#12Mpx
cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret_val, frame = cap.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)


    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1
    keyCode = cv2.waitKey(1)
    if keyCode == 27:
        break

cap.release()
cv2.destroyAllWindows()