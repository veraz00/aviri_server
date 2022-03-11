import sys 
import os 
from flask import request, make_response, Response, jsonify, current_app, g, send_from_directory, send_file, safe_join, abort
sys.path.append('..')
print('os.getcwd()', os.getcwd())
from app.api import blueprint
from controller.image import ImageController
from common.error import HttpError, exception_handler
from controller.prediction import PredictionController
from io import BytesIO
import cv2
from PIL import Image

os.environ['DATA_DIR'] = 'data'  
os.environ['INPUTS_DIR'] = 'inputs/20_images/'
os.environ['HEATMAP_DIR'] = 'heatmap/'
# not use absolute path!!
def image_to_str(img):  # img is RGB
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_byte = buffered.getvalue() # bytes
    img_base64 = base64.b64encode(img_byte) #Base64-encoded bytes * not str
    #It's still bytes so json.Convert to str to dumps(Because the json element does not support bytes type)
    img_str = img_base64.decode('utf-8') # str
    return img_str

@blueprint.before_request
def before_request_fn():
    g.image = ImageController()
    g.prediction = PredictionController()

import base64
@blueprint.route('v1/home')  # can be called
@exception_handler
def Home():
    return 'Hello, this is Linlin-server'


@blueprint.route('/v1/image', methods = ['POST'])  # api/vi/image  # done
@exception_handler
def createImage():
    # record = dict()
    # for file in os.listdir(os.environ['INPUTS_DIR']):
    #     record['filename'] = file
    #     with open(os.path.join(os.environ['INPUTS_DIR'], file), 'rb') as image1:
    #         record['content'] = base64.b64encode(image1.read())
    #         img = g.image.create(record)
    #         print('25 img', img)
    #         return 
    # print('request.headers', dict(request.headers))
#{'Host': '192.168.50.170:5050', 'User-Agent': 'python-requests/2.27.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', \
    # 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Content-Length': '1738033'}
    img = g.image.create(request.get_json())  # request.get_json()-- is it a dict of record?? how an external port like this??
    return jsonify(img), 200


@blueprint.route('/v1/image', methods=['GET'])  # done
@exception_handler
def get_images():
    imgs = g.image.query(request.args.to_dict())  # request would a dict with filtering information
    return jsonify(imgs), 200

@blueprint.route('/v1/image/<id>', methods=['PATCH'])  # get can be called, 
@exception_handler
def getImageById(id):
    if request.method == 'GET':    
        img = g.image.get(id)
        return jsonify(img), 200
    else:
        print('request.headers', request.headers)
        print('request.methods', request.method)
        g.image.update(id, request.get_json())
        return '', 200

@blueprint.route('/v1/image/<id>', methods=['DELETE'])  # the id returned ??
@exception_handler
def delete_image(id):
    g.image.delete(id)
    return "", 200


@blueprint.route('/v1/image/download/<path:image_id>', methods=['GET'])    # path = heatmapid / heatmap_filename.jpg
@exception_handler 
def download_image(image_id):
    aim_dir = os.path.join(os.environ['DATA_DIR'], image_id)
    filename = os.listdir(aim_dir)[0]
    img = cv2.imread(os.path.join(aim_dir, filename))
    try:
        return send_from_directory(directory=aim_dir, path = filename, as_attachment = True)  #  parameters 
    except FileNotFoundError:
        abort(404)
# g.image.config['] how to add it??

import time 
@blueprint.route('/v1/prediction/<id>/<model_name>', methods=['GET'])
@exception_handler
def generatePrediction(id, model_name):
    start = time.time()
    try:
        pred = g.prediction.get(filename_id = id, model_name = model_name)
    except HttpError as e:
        params = {'filename_id':id, 'model_name':model_name}
        pred = g.prediction.create(params)  
        end = time.time()
        print('time for generatePrediction() in route: ', end-start,'seconds')
    
    return jsonify(pred), 200

# @blueprint.route('/v1/prediction/<id>/<model_name>', methods=['GET'])
# @exception_handler
# def get_prediction(id, model_name):
#     img = 
#     return jsonify(img), 200

# download heatmap
# change api- heatmap download, picts??
# download, from OD, download OS; OD+OS
# heatmpa download


@blueprint.route('/v1/heatmap/download/<heatmap_name_id>', methods=['GET'])    # path = heatmapid / heatmap_filename.jpg
@exception_handler 
def download_heatmap(heatmap_name_id):
    aim_dir = os.path.join(os.environ['HEATMAP_DIR'], heatmap_name_id)
    print('aim_dir', aim_dir)
    for filename in os.listdir(aim_dir):
        print('125', filename)
        aim_path = os.path.join(aim_dir, filename)
        img = Image.open(aim_path).convert('RGB')
        img_str = image_to_str(img)
        
        return jsonify({'heatmap_content': img_str}), 200

 
@blueprint.route('/v1/auc', methods=['POST'])
@exception_handler
def create_auc():
    result = g.prediction.auc(request.get_json())
    return jsonify(result)