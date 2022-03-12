import os 
import time 
import uuid
import base64
from pathlib import Path
from sqlalchemy import Binary, Column, Integer, String, text
from sqlalchemy.orm.exc import NoResultFound
from app import db
from common.error import HttpError
from datetime import datetime 
from ai.image_check import is_imglist

from app.models import Image


class ImageController:
    def __init__(self):
        pass
    
    def get_filepath(self, id, filename = None):
        if filename ==None:
            image = self.get(id)
            filename = image['filename']  # wer_retina_os_20220202_101010.jpg, wer_retina_os_20220202_101010_heatmap.jpg, 
        if os.path.isabs(os.environ['INPUT_DIR']):
            filepath = os.path.join(os.environ['INPUT_DIR'], id, filename)
        else:
            filepath = os.path.join(os.getcwd(),os.environ['INPUT_DIR'], id, filename)
        if not os.path.isfile(filepath):
            filepath += Path(filename).suffix  # ??
        return filepath
    
    def write_file(self, id, filename, data):
        path = os.path.join(os.environ['INPUT_DIR'], id)
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(path):
            raise HttpError("Create file failed.", 500)
        f = open(os.path.join(path, filename), "wb")
        f.write(data)
        f.close()
        filepath = os.path.join(path, filename)
        err_dict = is_imglist([filepath])
        if isinstance(err_dict, dict):
            os.remove(filepath)
            os.rmdir(path)
            raise HttpError('%s' % err_dict['err_message'], 406)

    
    def delete_file(self, id, filename=None):
        os.remove(self.get_filepath(id, filename))  # do I need to remove the id directory??
        os.rmdir(os.path.join(os.environ['INPUT_DIR'], id))
        
    def create(self, record):  #  if the filename is the same as before; it would create a new one; instead of replacing the previous one??
        if record == None or 'content' not in record or 'filename' not in record:
            raise HttpError('Invalid request data', 400)
        # image checking 
        img = Image(id = uuid.uuid4().hex)        
        data = base64.b64decode(record["content"])  #  convert a imgstring into an image
        try:  # image checking 
            self.write_file(img.id, record["filename"], data)  # write image into input direction
        except HttpError as err:
            raise err
        
        for prop in dir(img):
            if prop.startswith("_"):
                continue
            if prop in record and prop in Image.create_fields:
                setattr(img, prop, record[prop])

        setattr(img, "size", len(data))
        setattr(img, "timestamp", datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        db.session.add(img)
        db.session.commit()

        return img.to_dict()
    
    def query(self, params):
        sql = "SELECT * FROM image"
        delimiter = " WHERE "
        cond = {}
        for p in params:
            if p in Image.all_fields:
                sql += delimiter + p+"=:"+p
                delimiter = " AND "
                cond[p] = params[p]
        if "_filter" in params:
            cond["filter"] = "%"+params["_filter"]+"%"
            fdelimiter = "("
            for field in Image.filter_fields:
                sql += delimiter + fdelimiter + field + " like :filter"
                delimiter = ""
                fdelimiter = " OR "
            sql += ")"

        imgs = Image.query.from_statement(text(sql)).params(**cond).all()
        return [ x.to_dict() for x in imgs ]
    
    def get(self, id):
        try:
            sql = 'select * from image where id=:id'
            img = Image.query.from_statement(text(sql)).params(id=id).one()
        except NoResultFound as e:
            raise HttpError('No image Found', 404)
        return img.to_dict()
    
    def update(self, id, record):
        try:
            sql = 'select * from image where id=:id'
            img = Image.query.from_statement(text(sql)).params(id=id).one()
        except NoResultFound as e:
            raise HttpError('No image found.', 404)
        
        if "content" in record:
            data = base64.b64decode(record["content"])
            try:
                self.write_file(img.id, getattr(img, "filename"), data)
            except HttpError as err:
                raise err
            setattr(img, "size", len(data))
            
        if "filename" in record:
            os.rename(self.get_filepath(id, img.filename), os.path.join(os.environ['INPUT_DIR'], id, record['filename']))

        for prop in dir(img):
            if prop.startswith("_"):
                continue
            if prop in record and prop in Image.update_fields:
                setattr(img, prop, record[prop])

        db.session.commit()

    def delete(self, id):
        try:
            sql = "SELECT * FROM image WHERE id=:id"
            img = Image.query.from_statement(text(sql)).params(id=id).one()
        except NoResultFound as e:
            raise HttpError("No image found.", 404)

        db.session.delete(img)
        db.session.commit()

        self.delete_file(id, getattr(img, "filename"))
