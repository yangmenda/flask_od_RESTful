# coding:utf-8
 
from flask import Flask,jsonify

from predict import P1
from pre_v import P2
from pre_dir import P3

import json
# from predict_video import detect
#设置允许的文件格式
from flask_restful import Resource,Api
app=Flask(__name__)
from flasgger import Swagger

actual_w_DEFAULT=128
actual_h_DEFAULT=73

Swagger(app)

@app.route('/predict_image', methods=['GET'])

def index1():
    """
    
    预测单张图片API(预测前请确保待预测图片放置于系统目录下的images文件夹下)
    
    
    ---
    
    tags:
      - 预测单张图片API(预测前请确保待预测图片放置于系统目录下的images文件夹下)
    
      
    responses:
      500:
        description: 服务器内部错误！
      200:
        description: 系统正常运行!
        schema:
          
          properties:
            result_path:
              type: string
              description: 结果图片路径
              default: /static/images/predict.jpg
            log_path:
              type: string
              description: 包含图片的检测数量，位置的文件路径
              default: /static/logs/logs.txt
            image:
              type: string
              description: 待预测图片是否存在
              default: ok!
            detection:
              type: string
              description: 检测是否完成
              default: done
            object_numbers:
              type: string
              description: 检测出的枯死树数量
              default: 实际检测数量，是一个数字
            
            
            
            
    """
    p1=Predict_img()
    
    return p1.get()
@app.route('/predict_video', methods=['GET'])
def index2():
    """
    预测单条视频API(预测前请确保待预测视频放置于系统目录下的videos文件夹下)
    
    ---
    tags:
      - 预测单条视频API(预测前请确保待预测视频放置于系统目录下的videos文件夹下)
    
    responses:
      500:
        description: 服务器内部错误!
      200:
        description: 系统正常运行!
        schema:
          
          properties:
            video:
              type: string
              description: 待预测视频是否存在
              default: ok!
            result_path:
              type: string
              description: 结果视频路径
              default: /static/images/predict.mp4
            log_path:
              type: string
              description: 包含视频的检测数量，位置的文件路径
              default: /static/logs/logs.txt
            detection:
              type: string
              description: 检测是否完成
              default: done
            object_numbers:
              type: string
              description: 检测出的枯死树数量
              default: 实际检测数量，是一个数字
            
    """
    p2=Predict_video()
    return p2.get()
        
        
    

api=Api(app)
class Predict_img(Resource):
    def __init__(self):
        
        pass

       
    def get(self):
        v,d,n=P1()
        n_s=str(n)
        if v and d:
            return jsonify({
                "image":"ok!",
                "detection":"done",
                "result_path":"/static/images/predict.jpg",
                "log_path":"/static/logs/logs.txt",
                "object_numbers":n_s
            })
        if v:
            return jsonify({
                "image":"ok!",
                "detection":"not done",
                "result_path":"None",
                "log_path":"None",
                "object_numbers":"0"
            })
        else:
            return jsonify({
                "image":"not exisit!",
                "detection":"not done",
                "result_path":"None",
                "log_path":"None",
                "object_numbers":"0"
            })
        
class Predict_img_dir(Resource):
    def __init__(self):
        
        pass

    def get(self):
        e,d,c=P3()
        if e and d and c:
            return jsonify({
                "extract":"done",
                "detection":"done",
                "compress":"done",
                "result_path":"/static/predictions.zip",
                
            })
        if e and d:
            return jsonify({
                "extract":"done",
                "detection":"done",
                "compress":"fail",
                "result_path":"None",
                
            })
        if e :
            return jsonify({
                "extract":"done",
                "detection":"not done",
                "compress":"fail",
                "result_path":"None",
                
            })
        else:
            return jsonify({
                "extract":"fail",
                "detection":"not done",
                "compress":"fail",
                "result_path":"None",
                
            })

class Predict_video(Resource):
    def __init__(self):
        pass
    def get(self):
        v,d,n=P2()
        n_s=str(n)
        if v and d:
            return jsonify({
                "video":"ok!",
                "detection":"done",
                "result_path":"/static/videos/predict.mp4",
                "log_path":"/static/logs/logs.txt",
                "object_numbers":n_s
            })
        if v:
            return jsonify({
                "video":"ok!",
                "detection":"not done",
                "result_path":"None",
                "log_path":"None",
                "object_numbers":"0"
            })
        else:
            return jsonify({
                "video":"not exisit!",
                "detection":"not done",
                "result_path":"None",
                "log_path":"None",
                "object_numbers":"0"
            })


api.add_resource(Predict_img,'/predict_image')
api.add_resource(Predict_video,'/predict_video')
api.add_resource(Predict_img_dir,'/predict_image_dir')
if __name__ == '__main__':
    # app.debug = True
   
    app.run(host='0.0.0.0', port=7000, debug=True)
    

