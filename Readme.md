# Aviri_server
This is an ai_server to provide VI disease prediction based on VI_CNN model.

## Folder structure
ai: ai model
samples: 20 images is downloaded from kaggle dataset; the other 5 images are from Retina camera


## Steps to run AI server based on MAC
```
# python3.7 
pip install -r requirements.txt
python app.py  # create db.sqlite

# here I did not use migration in model, which is a necessity when running on windows; so suggest to run it on mac
```

## Curl command 
Example to curl api (Need to change ip address and id)

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



### Time for prediction images

1) load model: 10-12s
2) Time for get prediction per image:  0.8950 seconds <br>
- Time for get image:  0.0018 seconds <br>
- Loading models takes 5.8889e-05 seconds <br>
- Time for prediction: 0.7705 seconds <br>
- Time for writing in db:  0.01388 seconds <br>




