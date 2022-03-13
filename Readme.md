# Aviri_server
This is an ai_server to provide VI disease prediction based on VI_CNN model.

## Folder structure
ai: ai model
samples: 20 images is downloaded from kaggle dataset; the other 5 images are from Retina camera


## Steps to run AI server based on MAC
```
# python3.7 
python3.7 -m virtualenv py37-venv
source py37-venv/bin/activate
pip install -r requirements.txt
python app.py  # create db.sqlite

# here I did not use migration in model, which is a necessity when running on windows; so suggest to run it on mac
```

## Curl command 
Example to curl api (Need to change ip and image_id)
```
# create fake image 
curl -X GET \
-H "Accept: application/json" \
"http://<ip>/api/v1/home"  


# get image 
curl -X GET \
-H "Accept: application/json" \
"http://<ip>/api/v1/image?id=<image_id>"


# delete image 
curl -X DELETE \
-H "Content-Type: application/json" \
"http://<ip>/api/v1/image/<image_id>"


# download image 
curl -X GET \
-H "Accept: application/json" \
"http://<ip>/api/v1/image/download/<image_id>"


# get prediction/create prediction if filename not exists before
curl -X GET \
-H "Content-Type: application/json" \
"http://<ip>/api/v1/prediction/<image_id>/VI_CNN"


# download heatmap
curl -X GET \
-H "Accept: application/json" \
"http://<ip>/api/v1/heatmap/download/<heatmap_id>"
```


### Time for prediction images

1) load model: 10-12s
2) Time for get prediction per image:  0.8950 seconds <br>
  - Time for get image:  0.0018 seconds <br>
  - Loading models takes 5.8889e-05 seconds <br>
  - Time for prediction: 0.7705 seconds <br>
  - Time for writing in db:  0.01388 seconds <br>




