##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed
import serial
from datetime import datetime
import cv2 as cv
import os


n_frames = 1000
serial_port = '/dev/ttyUSB0'
baud_rate = 19200 #In arduino, Serial.begin(baud_rate)
path = "/media/sdb/MotionAndVisionIntegrationData/"


# What better place than here?
# What better time than now?
right_now = datetime.now()

timestamp = right_now.isoformat()
write_to_path = path + timestamp
write_to_img_path = write_to_path + "/img/"
write_to_file_path = write_to_path + "/" + "output.txt"

cap = cv.VideoCapture(0)
cap.set(4, 240)
cap.set(3, 320)
cap.set(5, 60)


frame_list = []
out_list = []

with serial.Serial(serial_port, baud_rate) as ser:
    for _ in range(n_frames):
        ser.write("0".encode())
        line = ser.readline()
        line = line.decode("utf-8")
        line_time_stamp = datetime.now()
        ret, frame = cap.read()
        frame_time_stamp = datetime.now()
        print(line + 'at ' + line_time_stamp.isoformat(' '))
        print('Frame captured at ' + frame_time_stamp.isoformat(' '))
        out_list.append(line_time_stamp.isoformat('-') + ', ' + line)
        frame_list.append((write_to_img_path +
                           frame_time_stamp.isoformat("-") + '.png',
                           frame))



dir_list = os.listdir(path)

if timestamp not in dir_list:
    os.mkdir(write_to_path)
    os.mkdir(write_to_img_path)
else:
    data_list = os.listdir(write_to_path)
    if "img" not in data_list:
        os.mkdir(write_to_img_path)

with open(write_to_file_path, "w+") as output_file:
    for ((fname, frame), line)  in zip(frame_list, out_list):
        cv.imwrite(fname, frame)
        output_file.write(line)
