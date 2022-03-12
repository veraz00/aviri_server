from genericpath import exists
import sys 
import os 
from flask import request, make_response, Response, jsonify, current_app, g, send_from_directory, send_file, safe_join, abort
sys.path.append('..')
print('os.getcwd()', os.getcwd())  # so the system path: aviri_server
from app.api import blueprint
from controller.image import ImageController
from common.error import HttpError, exception_handler
from controller.prediction import PredictionController
from io import BytesIO
import cv2
from PIL import Image
import time 
import base64


if not os.path.exists('input'):
    os.makedirs('input', exist_ok=True)  # dir: ai

if not os.path.exists('heatmap'): 
    os.makedirs('heatmap', exist_ok=True) 

os.environ['INPUT_DIR'] = 'input/'
os.environ['SAMPLE_DIR'] = 'samples/20_images/'
os.environ['HEATMAP_DIR'] = 'heatmap/'


def image_to_str(img):  # img is RGB
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_byte = buffered.getvalue() # bytes
    img_base64 = base64.b64encode(img_byte) #Base64-encoded bytes, not str

    img_str = img_base64.decode('utf-8') # str: Because the json element does not support bytes type
    return img_str

@blueprint.before_request
def before_request_fn():
    g.image = ImageController()
    g.prediction = PredictionController()


@blueprint.route('v1/home')  
@exception_handler
def Home():
    return 'Hello, this is AVIRI-SERVER'


@blueprint.route('/v1/image', methods = ['POST'])  # api/vi/image  
@exception_handler
def createImage():

    img = g.image.create(request.get_json())  
    return jsonify(img), 200


@blueprint.route('/v1/image', methods=['GET'])  
@exception_handler
def get_images():
    imgs = g.image.query(request.args.to_dict())  
    return jsonify(imgs), 200


@blueprint.route('/v1/image/<id>', methods=['PATCH', 'GET'])  
@exception_handler
def getImageById(id):
    if request.method == 'GET':    
        img = g.image.get(id)
        return jsonify(img), 200
    else:
        g.image.update(id, request.get_json())
        return '', 200


@blueprint.route('/v1/image/<id>', methods=['DELETE'])  
@exception_handler
def delete_image(id):
    g.image.delete(id)
    return "", 200


@blueprint.route('/v1/image/download/<image_id>', methods=['GET'])    
@exception_handler 
def download_image(image_id):
    aim_dir = os.path.join(os.environ['DATA_DIR'], image_id)
    for filename in os.listdir(aim_dir):
        aim_path = os.path.join(aim_dir, filename)
        img = Image.open(aim_path).convert('RGB')
        img_str = image_to_str(img)
        
        return jsonify({'image_content': img_str}), 200


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
        print('AI server time for generatePrediction() in route: ', end-start,'seconds')
    return jsonify(pred), 200



@blueprint.route('/v1/heatmap/download/<heatmap_name_id>', methods=['GET'])   
@exception_handler 
def download_heatmap(heatmap_name_id):
    aim_dir = os.path.join(os.environ['HEATMAP_DIR'], heatmap_name_id)
    for filename in os.listdir(aim_dir):
        aim_path = os.path.join(aim_dir, filename)
        img = Image.open(aim_path).convert('RGB')
        img_str = image_to_str(img)    
        return jsonify({'heatmap_content': img_str}), 200

 
@blueprint.route('/v1/auc', methods=['POST'])  # Not test yet??
@exception_handler
def create_auc():
    result = g.prediction.auc(request.get_json())
    return jsonify(result)