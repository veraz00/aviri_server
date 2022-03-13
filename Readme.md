# Aviri_server
This is a ai_server to provide VI disease prediction based on VI_CNN model.

## Steps to run AI server using python3.7 based on MAC
```
pip install -r requirements.txt
python app.py  # create db.sqlite
```

## Curl command 
Need to change ip address and id
- create fake image 
curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/home"  


- get image 
curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/image?id=e468c4d3ad8b4cbebcb93e4f8117c7d4"


- delete image 
curl -X DELETE \
-H "Content-Type: application/json" \
"http://192.168.50.170:5050/api/v1/image/0aa537b09c5c4d8ab482877c7f0635a8"


- download image 
curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/image/download/e468c4d3ad8b4cbebcb93e4f8117c7d4"


- get prediction/create prediction if filename exists before
curl -X GET \
-H "Content-Type: application/json" \
"http://192.168.50.170:5050/api/v1/prediction/e468c4d3ad8b4cbebcb93e4f8117c7d4/VI_CNN"


- download heatmap
curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/heatmap/download/5b53431e58b146ce82dfb02ee35f9192"



## Folder examplanation
samples: 20 images is downloaded from kaggle dataset; the other 5 images are from Retina camera


## Time for prediction images
1) load model: 10-12s
2) prediction
time for get image:  0.0018 seconds
Loading models takes 5.8889e-05 seconds
time for prediction: 0.7705 seconds
time for writing in db:  0.01388 seconds
==>time for generatePrediction() per image after loading model:  0.8950 seconds



