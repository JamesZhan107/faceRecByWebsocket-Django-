#-*-coding:utf8-*-
import os
import cv2
import numpy as np
import face_recognition
from readimg import read_img
import scipy.misc
#输入一个文件路径，对其下的每个文件夹下的图片读取并face_encoding，并对每个文件夹给一个不同的Label
#返回一个img的list,返回一个对应label的list.
def read_file(path):
    label_list = []
    dir_counter = 0

    #二维数组存储每个子文件夹下每张图片的face_encoding.
    img_encoding = [[] for i in range(15)]
    for child_dir in os.listdir(path):
         child_path = os.path.join(path, child_dir)

         for dir_image in  os.listdir(child_path):

             if read_img.endwith(dir_image,'jpg'):
                img = scipy.misc.imread(os.path.join(child_path, dir_image))
                #resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                #recolored_img = cv2.cvtColor(resized_img,cv2.COLOR_BGR2GRAY)
                print("到这1")
                img_encoding[dir_counter].append(face_recognition.face_encodings(img)[0])
                label_list.append(dir_counter)
         dir_counter += 1


    return img_encoding,label_list,dir_counter

#读取训练数据集的文件夹，把他们的名字返回给一个list
def read_name_list(path):
    name_list = []
    for child_dir in os.listdir(path):
        name_list.append(child_dir)
    return name_list


#测试
if __name__ == '__main__':
    img_list,label_lsit,counter = read_file('../dataset')
    tt  = read_name_list('../dataset')
    print (img_list,label_lsit,counter)
    print (tt)
