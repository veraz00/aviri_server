from sqlalchemy import Binary, Column, Integer, String, text, Float
from sqlalchemy.orm.exc import NoResultFound
from app import db

class Image(db.Model):
    __tablename__ = 'image'

    id = Column(String, primary_key=True)
    filename = Column(String)
    size = Column(Integer)
    timestamp = Column(String)

    all_fields = [ "id", "filename", "size", "timestamp" ]
    create_fields = ["filename"]
    update_fields = ["filename"]
    filter_fields = ["filename"]

    def __repr__(self):
        return str(self.name)

    def to_dict(self):
        ret = {}
        for prop in dir(self):
            if prop.startswith("_") or prop not in Image.all_fields:
                continue
            ret[prop] = getattr(self, prop)
        return ret


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