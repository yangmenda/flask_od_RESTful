from ftplib import FTP
import sys
import os
import requests
import json
option=sys.argv[1]
ftp_ip = "192.168.0.119"
ftp_port = 21  
ftp_user = "nvidia"
ftp_password = "nvidia"
path="/home/nvidia/AI_tree/"
filename=sys.argv[2]
file_path=os.path.join("./"+filename)
url='http://192.168.0.119:7000'



if option=="predict_image":
    op="/"+option
    location=path+"images/"
if option=="predict_video":
    op="/"+option
    location=path+"videos/"
if option=="predict_image_dir":
    op="/"+option
    location=path+"images_dir/"

def file_transfer():
    ftp=FTP()
    ftp.connect(ftp_ip,ftp_port)
    ftp.login(ftp_user,ftp_password)

    remote_path=os.path.join(location+filename)

    bufsize = 1024
    try:
        with open(file_path,'rb') as fp:
            ftp.storbinary('STOR ' +remote_path,fp,bufsize)
            ftp.set_debuglevel(0)
            upload_done=True
            print("File upload success!")
    except Exception as e:
        print(e)
        upload_done=False
    return upload_done

def get_predict():
    url_api=url+op
    with requests.get(url_api) as r:
        req_json=r.json()
        doc=req_json
    
    if option=="predict_image_dir":
        if doc["detection"]=="done":
                print("Detection complete!")
        if doc["result_path"] !="None":
            
            url_download=url+doc["result_path"]
    
            with requests.get(url_download) as res:
                with open("./prediction.zip","wb") as f:
                    f.write(res.content)
                    f.close()
            print("Download complete!")
                
        else:
            print("test fail!")
    if option=="predict_video":
        if doc["detection"]=="done":
                print("Detection complete!")
        if doc["result_path"] !="None":
            
            url_video=url+doc["result_path"]
            url_log=url+doc["log_path"]
            with requests.get(url_video) as res:
                with open("./prediction.mp4","wb") as f:
                    f.write(res.content)
                    f.close()
            with requests.get(url_log) as res:
                with open("./logs.txt","wb") as f:
                    f.write(res.content)
                    f.close()
            print("Download compltete!")
            
        else:
            print("test fail!")
    else:
        if doc["detection"]=="done":
                print("Detection complete!")        
        if doc["result_path"] !="None":
            
            url_image=url+doc["result_path"]
            url_log=url+doc["log_path"]
            with requests.get(url_image) as res:
                with open("./prediction.jpg","wb") as f:
                    f.write(res.content)
                    f.close()
            with requests.get(url_log) as res:
                with open("./logs.txt","wb") as f:
                    f.write(res.content)
                    f.close()
            print("Download compltete!")
    
        else:
            print("test fail!")

if __name__=="__main__":
    upload_ok=file_transfer()
    if upload_ok:
        get_predict()
    else:
        print("file transfer fail!")

