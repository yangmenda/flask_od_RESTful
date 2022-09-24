import zipfile
import os
from tqdm import tqdm
from PIL import Image
from yolo import YOLO

path="./images_dir/"
dir_save_path="./img_out_dir/"
e=False
d=False
c=False

def unzip():
    
    file_list=os.listdir(path)

    for f in file_list:
        f=f.lower()
        a=f.split('.')
        if a[1]=="zip":
            zip_file = zipfile.ZipFile(os.path.join(path,f))
            for names in zip_file.namelist():
                zip_file.extract(names, path)
            zip_file.close()
        file_dir=os.path.join(path,a[0])
    e=True
    os.remove(os.path.join(path,f))
    return file_dir,e

def Predict():
    yolo=YOLO()
    path1,e=unzip()
    img_names = os.listdir(path1)
    for img_name in tqdm(img_names):
            if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                image_path  = os.path.join(path1, img_name)
                image       = Image.open(image_path)
                r_image     = yolo.detect_image(image)
                if not os.path.exists(dir_save_path):
                    os.makedirs(dir_save_path)
                r_image.save(os.path.join(dir_save_path, img_name), quality=95, subsampling=0)
    d=True
    path_data=path1
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "/" + i#当前文件夹的下面的所有东西的绝对路径
        #os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
        os.remove(file_data)
    os.rmdir(path1)
    return d,e
def P3():
    d,e=Predict()
    if d==True:

        path2="./static/predictions.zip"
        if os.path.exists(path2):
            os.remove(path2)
        zipf = zipfile.ZipFile(path2, 'w',zipfile.ZIP_DEFLATED)
        
        for path,dirnames,filenames in os.walk(dir_save_path):
            fpath = path.replace(dir_save_path,'')

            for filename in filenames:
                zipf.write(os.path.join(path,filename),os.path.join(fpath,filename))
        zipf.close()
    c=True
    path_data=dir_save_path
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "/" + i#当前文件夹的下面的所有东西的绝对路径
        #os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
        os.remove(file_data)
        


    return e,d,c

    