import time
import threading
import base64
import uuid
import os
from flask import jsonify 
from sqlalchemy import Binary, Column, Integer, String, text, Float
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime 
from app import db
from common.error import HttpError
from .image import ImageController
from ai.aviri_main import get_aviri_prediction as do_prediction
from ai.aviri_main import get_aviri_AUC as calculate_auc

lock = threading.Lock()


os.environ['HEATMAP_DIR'] = './heatmap'

class Prediction(db.Model):
    __tablename__ = 'prediction'
    

    filename = Column(String)
    filename_id = Column(String, primary_key=True)
    result = Column(String, nullable=False)
    probability_VI0 = Column(Float, nullable=False)
    probability_VI1 =Column(Float, nullable=False)
    model_name = Column(String, primary_key=True, nullable=False)
    heatmap_name = Column(String)
    heatmap_name_id = Column(String)
    timestamp = Column(String)

    all_fields = [ "filename", "filename_id", "result", "probability_VI0", "prbability_VI1", \
        "model_name", "heatmap_name", "heatmap_name_id","timestamp" ]

    def __repr__(self):
        return str(self.heatmap_name)

    def to_dict(self):
        ret = {}
        for prop in dir(self):
            if prop.startswith("_") or prop not in Prediction.all_fields:
                continue
            ret[prop] = getattr(self, prop)
        return ret

import cv2
class PredictionController:
    def __init__(self):
        self.image = ImageController()
    
    def write_file(self, id, filename, data):  # write heatmap from numpy into jpg
        path = os.path.join(os.environ['HEATMAP_DIR'],id)
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(path):
            raise HttpError("Create file failed.", 500)

        cv2.imwrite(os.path.join(path, filename), data)
        return 

    def predict(self, img, model_name):
        lock.acquire()
        try:
            resp = do_prediction(
            img_locations = self.image.get_filepath(img["id"], img["filename"]),
            models_list = [model_name] #  ['VI'] ['VI_Moderate']
            )[0]
            #  resp  = {'heatmap_content': a numpy, 'heatmap_name': _heatmap.jpg}
        finally:
            lock.release()
        return resp

    def get(self, filename_id, model_name):

        try:
            sql = "SELECT * FROM prediction WHERE filename_id=:filename_id and model_name=:model_name"
            prediction = Prediction.query.from_statement(text(sql)).params({'filename_id':filename_id, 'model_name':model_name}).one()
        except NoResultFound as e:
            raise HttpError("No prediction found.", 404)

        ret = prediction.to_dict()
        ret["result"] = eval(ret["result"])

        return ret

    def create(self, params):
        if "filename_id" not in params or "model_name" not in params:  # only for a single model_name
            raise HttpError("Missing Field", 400)
        img = self.image.get(params["filename_id"]) 

        
        result = self.predict(img, model_name = params['model_name'])  
        try:
            sql = "SELECT * FROM prediction WHERE filename_id=:filename_id and model_name=:model_name"
            prediction = Prediction.query.from_statement(text(sql)).params({'filename_id':params["filename_id"], 'model_name':params['model_name']}).one()
        except NoResultFound as e:
            prediction = Prediction(filename_id = params['filename_id'], model_name=params['model_name'],\
        filename=img["filename"], heatmap_name_id = uuid.uuid4().hex)   
        
        try:
            self.write_file(prediction.heatmap_name_id, result['heatmap_name'], result['heatmap_content'])
        except HttpError as err:
            raise err 
        
            # write prediction content into folder, how to return it as a readable image type 
        # data = base64.b64decode(result['heatmap_content'])  # 
        setattr(prediction, "result", str(result['result']))
        setattr(prediction, "probability_VI0", result['proba_VI0'])
        setattr(prediction, "probability_VI1", result['proba_VI1'])
        setattr(prediction, "heatmap_name", str(result['heatmap_name']))
        setattr(prediction, "timestamp", datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))

        db.session.add(prediction)
        db.session.commit()
        return prediction.to_dict() #  it would be a dict

    def auc(self, params):  # default: model_list = ['VI_CNN']
        if params == None or "images" not in params or "labels" not in params:
            raise HttpError("Invalid request data.", 400)

        if len(params["images"]) != len(params["labels"]):
            raise HttpError("Invalid request data size.", 400)

        arg = []
        for i in range(len(params["images"])):
            img = self.image.get(params["images"][i])
            arg.append({
                "filepath": self.image.get_filepath(img["id"], img["filename"]),
                "label": params["labels"][i]
            })
            
        lock.acquire()
        try:
            result = calculate_auc(arg)
        finally:
            lock.release()
        return result