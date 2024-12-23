from django.shortcuts import render
from datetime import datetime,timedelta,date
from django.db import connection
from roboflow import Roboflow
import supervision as sv
import cv2
import time
import random
import numpy as np
from PIL import Image
from django.db import models


curr_dateTime = datetime.now()
curr_Time = datetime.now().strftime("%H:%M:%S")
curr_date = datetime.today().strftime("%Y-%m-%d")
cursor = connection.cursor()

global drName
drName = ''

global login
login = False

def test(request):
    return render(request,'userPortal.html')

def index(request):
    return render(request,'index.html')

def userLogin(request):
    return render(request,'userLogin.html')


def adminLogin(request):
    return render(request, 'adminLogin.html')

def userportal(request):
    global drName
    name = request.POST.get('user', drName)
    pword = request.POST.get('password', '')
    cursor.execute(''' select userId, userName, password from user where userName = %s''', [name])
    data = cursor.fetchone()

    drName = name

    global login
    
    if(login or data != None and name == data[1] and pword == data[2]):
        login = False
        param = {'name' : name.upper(), 'before' : 1}
        return render(request, 'userportal.html', param)
    else: 
        login = False
        param = {'flag' : 1, 'message' : 'Invalid username or password'}
        return render(request, 'userLogin.html',param)

def adminportal(request):
    admins = ['likhith', 'nehal', 'prajwal', 'pawan']
    name = request.POST.get('user','')
    pword = request.POST.get('password', '')

    cursor.execute(''' select userId, userName, password from user where userId != %s''',[20000])
    data = cursor.fetchall()
    
    if(name in admins and pword == 'bitcse'):
        param = {'data': data, 'idx': 1}
        return render(request,'adminPortal.html', param)
    else :
        param = {'flag' : 1, 'message' : 'Invalid username or password'}
        return render(request, 'adminLogin.html', param)
    print(login)


def remove(request, pk):
    cursor.execute(''' delete from user where userId = %s ''',[pk])
    cursor.execute(''' select userId, userName, password from user where userId != %s''',[20000])
    data = cursor.fetchall()
    param = {'data': data, 'idx': 1}
    return render(request,'adminPortal.html', param)
    
def addUser(request):
    name = request.POST.get('user','')
    pword = request.POST.get('password', '')

    cursor.execute(''' select userId from user;''')
    userId = sorted(cursor.fetchall())
    
    flag = 0
    for i in range(0, len(userId)-1):
        flag = 1
        id_ = int(userId[i][0])
        if (id_ + 1 != int(userId[i+1][0])) :
            userId = id_ + 1
            break
        elif i == len(userId)-2:
            userId = int(max(userId)[0]) + 1
            break

    if(not flag and len(userId) == 1) :
        userId = int(userId[0][0]) + 1

    cursor.execute(''' insert into user values( %s, %s, %s);''',[userId, name, pword])

    cursor.execute(''' select userId, userName, password from user where userId != %s''',[20000])
    data = cursor.fetchall()
    param = {'data': data, 'idx': 1}
    return render(request,'adminPortal.html', param)


def reports(request):
    image = request.POST.get('imageUpload')
    # print(image)

    file = request.FILES['imageUpload']
    # img = str(file.read())
    image_array = np.array(Image.open(file))
    # print(image_array)
    cv2.imwrite('.\\static\\images\\preview.jpg', image_array)
    print("image saved successfully") 

    global drName
    global login

    login = True

    rf = Roboflow(api_key="wXfTtmCD7jF3NgHNgoY8")
    project_1 = rf.workspace().project("lumbar-sponylolisthesis")
    model_classify = project_1.version(6).model
    project_2 = rf.workspace().project("spondlylolisthesis")
    model_mul_class = project_2.version('2').model

    image_dir = ".\\static\\images\\preview.jpg"

    # image_dir = "/content/drive/MyDrive/dataset/Lumbar Sponylolisthesis.v6-slip-detection-v3.0.yolokeras/valid/188_jpg.rf.d21a66e0a8c5ce6a561a2418a8ecaf8d.jpg"

    #  "/content/drive/MyDrive/dataset/Lumbar Sponylolisthesis.v6-slip-detection-v3.0.yolokeras/valid/fc45efa9adecad0e9535e8319212aa51_jpg.rf.7f50c2ff7c2cbf852bfec5a0bfc9490c.jpg"

    # "/content/drive/MyDrive/dataset/Lumbar Sponylolisthesis.v6-slip-detection-v3.0.yolokeras/train/188ef8a3609e4a41cc420233fa1feedc_jpg.rf.a859132ea3912954f9e9339e72406283.jpg"

    #  "/content/drive/MyDrive/dataset/Spondylolisthesis.v2-v2.multiclass/valid/Screenshot-2022-07-31-050630_jpg.rf.6bfb7ca4b3acbebadd05a802bcbb824e.jpg"

    # img = cv2.imread('./static/preview.png')
    spondy = []
    vertebre = []

    occurance = []
    grades = ['GRADE_1', 'GRADE_2', 'GRADE_3', 'GRADE_4']

    # from inference_sdk import InferenceHTTPClient
    # CLIENT = InferenceHTTPClient(
    #     api_url="https://detect.roboflow.com",
    #     #api_key="wXfTtmCD7jF3NgHNgoY8" #nehal
    #     api_key="h6bvtXgivU9qEsIYdLAe" # likhith
    # )
    #to check wheather spondylolisthesis present or not
    result_ = model_classify.predict(image_dir, confidence=40, overlap=40).json()

    # to display the annoted image
    def showImage(result, labels):
        detections = sv.Detections.from_roboflow(result)

        label_annotator = sv.LabelAnnotator()
        box_annotator = sv.BoxAnnotator()

        image = cv2.imread(image_dir)
        print(labels)

        annotated_image = box_annotator.annotate(scene=image, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels)
        if len(labels) == 1:
            cv2.imwrite('.\\static\\images\\spond.jpg', annotated_image) 
        else:
            cv2.imwrite('.\\static\\images\\vertebre.jpg', annotated_image) 
        sv.plot_image(image=annotated_image, size=(8, 10))

    #to get the vertebre caused spondy
    def box_coordinates(predictions):
        for bounding_box in predictions:
            x1 = bounding_box['x'] - bounding_box['width'] / 2
            x2 = bounding_box['x'] + bounding_box['width'] / 2
            y1 = bounding_box['y'] - bounding_box['height'] / 2
            y2 = bounding_box['y'] + bounding_box['height'] / 2
            box = (x1, x2, y1, y2, bounding_box['width'], bounding_box['class'])
            if bounding_box['class'] == 'Spondylolisthesis':
                spondy.append(box)
            else :
                vertebre.append(box)


    # branch based on present or absent of spondy
    if len(result_['predictions']) > 0:
        result = model_classify.predict(image_dir, confidence=40, overlap=40).json()
        print(result)
        labels = [item["class"] for item in result["predictions"]]
        showImage(result, labels)
        box_coordinates(result['predictions'])

        result = model_mul_class.predict(image_dir, confidence=40, overlap=40).json()
        print(result)

        if(len(result['predictions']) > 0):
            labels = [item["class"] for item in result["predictions"]]
            box_coordinates(result['predictions'])
            showImage(result, labels)

            # loop and find the vertebre where spondy occured
            for vert in vertebre:
                if vert[0] > (spondy[0][0]-10)  and vert[1] < (spondy[0][1]+10) and vert[2] > (spondy[0][2]-10) and vert[3] < (spondy[0][3]+10):
                    occurance.append(vert)
                print(vert)


            if len(occurance) == 1 and occurance[0][-1] == 'L5': # for l5 and s1
                for vert in vertebre :
                    if vert[-1] == 'S1':
                        occurance.append(vert)
                        break

            print("----", spondy,'\n')
            print(" ------------------------------------------------------ ")
            print("           Spondylolisthesis occured between            ")
            print("                     ", end = '')
            for i in occurance :
                print('-', i[-1], '-' , end = '')
            print('\n-------------------------------------------------------')
            print(occurance)
            
            if len(occurance) >= 2: # for other vertebre
                up_ver, lower_ver = (occurance[0],occurance[1]) if occurance[0][3] < occurance[1][3] else (occurance[1], occurance[0])
                print("upper : ", up_ver)
                print("lower : ", lower_ver)
                percent = 0
                if(up_ver[0] > lower_ver[0]):
                    percent = (abs(up_ver[0] - lower_ver[0])/lower_ver[-2]) * 100
                else :
                    percent = (abs(up_ver[1] - lower_ver[1])/lower_ver[-2]) * 100

                percent = round(percent, 3)
                print("----------------------------------------------")
                print("    Percentage slip : ", percent)
                print("")

                # detect grade
                grade_idx = -1
                if(percent > 75):
                    grade_idx = 3
                elif(percent > 50):
                    grade_idx = 2
                elif(percent > 25):
                    grade_idx = 1
                else :
                    grade_idx = 0

                print(" ---------------  ", grades[grade_idx], " ----------------")
                print("          ",end = "")

    else :
        print(" ------------------------------------------------------ ")
        print("                      N O R M A L                       ")
        print(" ------------------------------------------------------ ")
        report = 'Spondylolisthesis occured in lumbar region'
        param = {'occured': 0, 'name' : drName.upper(), 'report': 'report generated', 'report' : report}
        return render(request, 'userPortal.html', param)

    report = 'Spondylolisthesis occured in lumbar region between vertebra '
    param = {'occured': 1, 'name' : drName.upper(), 'report': 'report generated', 'occ1' : occurance[0][-1], 
    'occ2': occurance[1][-1], 'slip' : percent , 'grade' : grades[grade_idx], 'report' : report, 'severe' : 0 if grade_idx <= 1 else 1}
    return render(request, 'userPortal.html', param)