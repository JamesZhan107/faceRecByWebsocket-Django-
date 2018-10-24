from django.shortcuts import render, redirect
from dwebsocket.decorators import accept_websocket, require_websocket
import numpy as np
import cv2
from detect_rec import detect
from detect_rec import recognition
from create_newdir import createdir
import random
from .forms import RegisterForm


def huanying(request):
    return render(request, 'huanying.html')
def index(request):
    return render(request, 'zhuye.html')
def index1(request):
    return render(request, 'caiji.html')
def index2(request):
    return render(request, 'jiance.html')
def index3(request):
    return render(request, 'shibie.html')
def login(request):
    return render(request, 'registration/login.html')

def register(request):
    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)
        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()
            # 注册成功，跳转回系统首页
            return redirect('/index/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()
    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'users/register.html', context={'form': form})

@accept_websocket
def echo2(request):
    global message_part1, message_part2
    while True:
        message1 = request.websocket.wait()
        if message1==None:
                pass
        else:
            a = message1.find(b'\xff\xd8' )
            b = message1.find(b'\xff\xd9' )
            if a != -1 and b != -1:      # 能找到上述字符
                jpg = message1[a:b+2]
                imgweb = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                imghtml = cv2.imencode('.jpg', imgweb)[1].tostring()
                request.websocket.send(imghtml)
            else:
                if a != -1 and b == -1:  # 字符前半段
                    message_part1 = message1

                if a == -1 and b != -1:  # 字符后半段
                    message_part2 = message1
                    message = message_part1 + message_part2
                    a = message.find(b'\xff\xd8' )
                    b = message.find(b'\xff\xd9' )
                    if a != -1 and b != -1:      # 能找到上述字符
                        jpg = message[a:b+2]
                        imgweb = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        imghtml = cv2.imencode('.jpg', imgweb)[1].tostring()
                        request.websocket.send(imghtml)


@accept_websocket
def caiji(request):
    global message_part1, message_part2, path
    while True:
        message1 = request.websocket.wait()
        if message1==None:
                pass
        else:
            a = message1.find(b'\xff\xd8' )
            b = message1.find(b'\xff\xd9' )
            if a != -1 and b != -1:      # 能找到上述字符
                jpg = message1[a:b+2]
                imgweb = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                imghtml = cv2.imencode('.jpg', imgweb)[1].tostring()
                request.websocket.send(imghtml)
            else:
                if a == -1 and b == -1:
                    dirname = message1.decode('ascii')
                    path = "./dataset/"+dirname
                    createdir.mkdir(path)
                if a != -1 and b == -1:  # 找到图像前半段
                    message_part1 = message1
                if a == -1 and b != -1:  # 找到图像后半段
                    message_part2 = message1
                    message = message_part1 + message_part2
                    a = message.find(b'\xff\xd8' )
                    b = message.find(b'\xff\xd9' )
                    if a != -1 and b != -1:      # 能找到上述字符
                        jpg = message[a:b+2]
                        #  写入二进制数据
                        number = random.randint(0,10000)
                        f = open(path +"/"+str(number)+".jpg","wb")
                        f.write(jpg)
                        f.close()
                        imgweb = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        imghtml = cv2.imencode('.jpg', imgweb)[1].tostring()
                        request.websocket.send(imghtml)

@accept_websocket
def jiance(request):
    global message_part1, message_part2
    face = detect.facerec()
    while True:
        message1 = request.websocket.wait()
        if message1==None:
                pass
        else:
            a = message1.find(b'\xff\xd8' )
            b = message1.find(b'\xff\xd9' )
            if a != -1 and b != -1:      # 能找到上述字符
                jpg = message1[a:b+2]
                imgweb = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                img = face.pridict(imgweb)
                imghtml = cv2.imencode('.jpg', img)[1].tostring()
                request.websocket.send(imghtml)
            else:
                if a != -1 and b == -1:  # 字符前半段
                    message_part1 = message1
                if a == -1 and b != -1:  # 字符后半段
                    message_part2 = message1
                    message = message_part1 + message_part2
                    a = message.find(b'\xff\xd8' )
                    b = message.find(b'\xff\xd9' )
                    if a != -1 and b != -1:      # 能找到上述字符
                        jpg = message[a:b+2]
                        imgweb = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        img = face.pridict(imgweb)
                        imghtml = cv2.imencode('.jpg', img)[1].tostring()
                        request.websocket.send(imghtml)

@accept_websocket
def shibie(request):
    global message_part1, message_part2
    face = recognition.facerec()
    while True:
        message1 = request.websocket.wait()
        if message1==None:
                pass
        else:
            a = message1.find(b'\xff\xd8' )
            b = message1.find(b'\xff\xd9' )
            if a != -1 and b != -1:      # 能找到上述字符
                jpg = message1[a:b+2]
                imgweb = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                imghtml = cv2.imencode('.jpg', imgweb)[1].tostring()
                request.websocket.send(imghtml)
            else:
                if a != -1 and b == -1:  # 字符前半段
                    message_part1 = message1
                if a == -1 and b != -1:  # 字符后半段
                    message_part2 = message1
                    message = message_part1 + message_part2
                    a = message.find(b'\xff\xd8' )
                    b = message.find(b'\xff\xd9' )
                    if a != -1 and b != -1:      # 能找到上述字符
                        jpg = message[a:b+2]
                        imgweb = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        img = face.pridict(imgweb)
                        imghtml = cv2.imencode('.jpg', img)[1].tostring()
                        request.websocket.send(imghtml)

