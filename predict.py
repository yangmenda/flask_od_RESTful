
#coding=utf-8 



import cv2

from PIL import Image
import os

from yolo import YOLO

def P1(actual_w=128,actual_h=73):
    file_exisit=False
    detection_done=False
    path='./images/'
    ALLOWED_EXTENSIONS_IMG = ['png', 'jpg',  'bmp','jpeg']
    file_list=os.listdir(path)
    if(len(file_list)==0):
        
        return file_exisit,detection_done,0
    file_exisit=True
    
    for f in file_list:
        f_low=f.lower()
        a=f_low.split('.')
       
        if a[1] in ALLOWED_EXTENSIONS_IMG and f_low!="test.jpg":
            img=cv2.imread(os.path.join(path,f))
            cv2.imwrite(os.path.join(path,'test.jpg'), img)
            os.remove(os.path.join(path,f))
       
        else:
            os.remove(os.path.join(path,f))
            continue

    
    yolo=YOLO()
    if os.path.exists("./static/logs/logs.txt"):
        os.remove("./static/logs/logs.txt")
    file=open("./static/logs/logs.txt",'w')
    file.close()
    
    
    dir_origin_path = "./images/"
    dir_save_path   = "./static/images/"
    
    addr1="test.jpg"
    img = os.path.join(dir_origin_path,addr1)
    image = Image.open(img)
    st3=str("image ")
    with open("./static/logs/logs.txt","a",encoding="utf-8") as file1:
        file1.write(st3)
    r_image,numbers = yolo.detect_image(image,count=True,index=0)
    addr2="predict.jpg"
    r_image.save(os.path.join(dir_save_path, addr2))
    detection_done=True
    with open("./static/logs/logs.txt","a",encoding="utf-8") as file1:
        file1.write("\n")
    with open("./static/logs/logs.txt","a",encoding="utf-8") as file1:
        file1.write("The total number of sick trees of this image is "+str(numbers))
    if os.path.exists(os.path.join(path,"test.jpg")):
        os.remove(os.path.join(path,"test.jpg"))
    return file_exisit,detection_done,numbers

        
   
            
            

    

    
	

