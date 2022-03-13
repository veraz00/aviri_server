Steps to run AI server based on python3.7
vir  # create virtual env python3.7
pip install -r requirements.txt
mkdir ai/model_files ## then add 3 model files into this folder 

python app.py  # create db.sqlite

# create fake image 
call api: 
curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/home"  


# get image 

curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/image?id=e468c4d3ad8b4cbebcb93e4f8117c7d4"

curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/image/e468c4d3ad8b4cbebcb93e4f8117c7d4"

# delete image 

curl -X DELETE \
-H "Content-Type: application/json" \
"http://192.168.50.170:5050/api/v1/image/0aa537b09c5c4d8ab482877c7f0635a8"


# download image 
curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/image/download/e468c4d3ad8b4cbebcb93e4f8117c7d4"


# get prediction/create prediction if filename exists before
curl -X GET \
-H "Content-Type: application/json" \
"http://192.168.50.170:5050/api/v1/prediction/e468c4d3ad8b4cbebcb93e4f8117c7d4/VI_CNN"


# download heatmap
curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/heatmap/download/5b53431e58b146ce82dfb02ee35f9192"



# Setting on AI 
samples: 20 images is downloaded from kaggle dataset; the other 5 images are from Retina camera

load model: 10- 12s
time for get image:  0.0018551349639892578
Loading models takes 5.888938903808594e-05 seconds
time for prediction: 0.7704911231994629
time for writing in db:  0.013881921768188477
==>time for generatePrediction() in route:  0.8949921131134033 seconds



