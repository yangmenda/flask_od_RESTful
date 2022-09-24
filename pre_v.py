

import cv2
import numpy as np
from PIL import Image
import os
import time
from yolo import YOLO

yolo=YOLO()
video_path="./videos/test.mp4"
video_save_path="./static/videos/predict.mp4"
video_fps= 30

def P2(actual_w=128,actual_h=73):
    file_exisit=False
    detection_done=False
    path='./videos/'
    ALLOWED_EXTENSIONS_video = ['mp4']
    
    file_list=os.listdir(path)
    if(len(file_list)==0):
        
        return file_exisit,detection_done,0
    file_exisit=True
    for f in file_list:
        f_low=f.lower()
        a=f_low.split('.')
        if a[1] in ALLOWED_EXTENSIONS_video and f_low!="test.mp4":
            cap = cv2.VideoCapture(os.path.join(path,f))
            
            
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            out = cv2.VideoWriter(os.path.join(path,'test.mp4'), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,(frame_width, frame_height))
            while (True):

            
                ret, frame = cap.read()
                if ret == True:

               
                    out.write(frame)  
                else:
                    break

            print("转化完成")        
            cap.release()
            out.release()
            os.remove(os.path.join(path,f))   
        else:
            os.remove(os.path.join(path,f))
            continue
    capture = cv2.VideoCapture(video_path)
    if video_save_path != "":
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        out = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)

    fps = 0.0
    if os.path.exists("./static/logs/logs.txt"):
        os.remove("./static/logs/logs.txt")
    file=open("./static/logs/logs.txt",'w')
    file.close()
    t1=time.time()
    print("Detection begins!")
    i=0
    numbers_total=0
    numbers_this=0
    numbers_prev=0
    while (True):
        
        # 读取某一帧
        ref, frame = capture.read()
        if ref==True:
        # 格式转变，BGRtoRGB
            i+=1
            sti=str(i)
            st3=str("frame "+sti)
            with open("./static/logs/logs.txt","a",encoding="utf-8") as file1:
                file1.write(st3)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 转变成Image
            frame = Image.fromarray(np.uint8(frame))
            # 进行检测
            frame,numbers=yolo.detect_image(frame,count=True,index=i)
            frame = np.array(frame)
            
            numbers_this=numbers
            
            if numbers_this>numbers_prev:
                numbers_total+=(numbers_this-numbers_prev)
            else:
                numbers_total=numbers_total
            
            numbers_prev=numbers_this
            # RGBtoBGR满足opencv显示格式
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)
            with open("./static/logs/logs.txt","a",encoding="utf-8") as file1:
                file1.write("\n")
        else:
            break
    with open("./static/logs/logs.txt","a",encoding="utf-8") as file1:
        file1.write("The total number of sick trees of this video is "+str(numbers_total))
    t2=time.time()
    dec=t2-t1
    print("Detection over!")
    print("本次视频检测用了：",dec)
    detection_done=True
        
        


    capture.release()
    out.release()
    cv2.destroyAllWindows()
    if os.path.exists(os.path.join(path,"test.mp4")):
        os.remove(os.path.join(path,"test.mp4"))
    return file_exisit,detection_done,numbers_total

