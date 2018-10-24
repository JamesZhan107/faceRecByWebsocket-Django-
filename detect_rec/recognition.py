# -*- coding: utf-8 -*-
# 利用开源库face_recognition进行人脸检测及识别

import face_recognition
import cv2
from readdata import read_data
import time

class facerec(object):
    def __init__(self):
        self.all_encoding, self.lable_list, self.counter = read_data.read_file('./dataset')
        self.name_list = read_data.read_name_list('./dataset')
    def pridict(self, img):
        face_names = []
        # 若输入为图像路径
    #    frame = face_recognition.load_image_file(img)

        # 若输入为图像数组
        frame = img
        known_image = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        face_locations = face_recognition.face_locations(known_image)

        a1 = time.time()
        face_encodings = face_recognition.face_encodings(known_image, face_locations)
        #匹配，并赋值
        a2 = time.time()
    #    print("编码时间", a2 - a1)
        for face_encoding in face_encodings:
            i = 0
            j = 0
            for t in self.all_encoding:
                for k in t:
                    match = face_recognition.compare_faces([k], face_encoding, tolerance=0.4)
                    if match[0]:
                        name = self.name_list[i]
                    #    print(name)
                        j=1
                i = i+1
            if j == 0:
                name = "unknown"
            face_names.append(name)


        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255),  2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left+6, bottom-6), font, 1.0, (255, 255, 255), 1)

        return frame

if __name__ == '__main__':
    img = "duoren.jpg"
    face = facerec()
    b = time.time()
    face.pridict(img)
    d = time.time()
    print(b-d)