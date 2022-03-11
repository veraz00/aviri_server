ctrl+ d exit from sqlite3
flask db init
flask db upgrade
flask run

#  convert image into base64: https://base64.guru/converter/encode/image

curl -X POST \
-H "Content-Type: application/json" \
-d '{"filename":"wer_retina_os_20222222_111123.jpg",
"content":"/"}' \
"http://192.168.50.170:5050/api/v1/image"  

curl -X POST \
-H "Content-Type: application/json" \
-d '{"filename":"tyj_retina_od_20211111_100000.jpg",
"content":"replace it with base64 encoded image"}' \
"http://192.168.50.170:5050/api/v1/image"


curl -X GET \
-H "Accept: application/json" \
-d '{"id": "8705a944cc2449338955a752fa52a549"}' \
"http://192.168.50.170:5050/api/v1/image?filename=103_left_cateract.jpg"  &id=1223443

curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/image/2aa7ccd5f7334ead90c5170ae62ceca2"


curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/image/2aa7ccd5f7334ead90c5170ae62ceca2"


curl -X PATCH \
-H "Content-Type: application/json" \   
-d '{"filename":"tyj_retina_od_20211111_040515.jpg"}' \
"http://192.168.50.170:5050/api/v1/image/3b90b809e1064350a45809cf922880b5"  
# if it is GET -H: "Accept: "


# request.get_json(): some can pick para from http, some can pick from json dict??


#  update image 
curl -X PATCH \
-H "Content-Type: application/json" \
-d '{"filename":"tyj_retina_od_20211111_040515.jpg",
"content":"today it is a raining day but it can be sunny afternoon, then at night, it becomes dark, deep dark."}' \
"http://192.168.50.170:5050/api/v1/image/0ae2097d863345e790de52653dbf288b"

# download image 

curl -O http://192.168.50.170:5050/api/v1/image/download/2aa7ccd5f7334ead90c5170ae62ceca2/2_right_prolifer.jpg

# delelte image 
curl -X DELETE \
-H "Content-Type: application/json" \
"http://192.168.50.170:5050/api/v1/image/2aa7ccd5f7334ead90c5170ae62ceca2"



# create prediction/ update prediction if filename exists before
curl -X POST \
-H "Content-Type: application/json" \
-d '{"filename_id":"5382f7caadc9471696cf5e437d01e046",
"model_name":"VI_CNN"}' \
"http://192.168.50.170:5050/api/v1/prediction"


# get prediction   filename_id/VI_CNN
curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/api/v1/prediction/8a4164bf437c4bafafa2d7df9a18f239/VI_CNN"

# download heatmap 
curl -X GET \
-H "Accept: application/json" \
http://192.168.50.170:5050/api/v1/heatmap/download/1cfca0e38da44cc09c46a579f350c8f1

curl -O http://192.168.50.170:5050/api/v1/prediction/download/1cfca0e38da44cc09c46a579f350c8f1/103_right_normal_heatmap.jpg

/Users/zenglinlin/Dev/linlin-server/heatmap/
# data app
curl -X GET \
-H "Accept: application/json" \
"http://192.168.50.170:5050/data/d7c3bccbda141e1854d735a1eeee26e/input"


# # get an image and return a id; use id to get prediction 
# # module test: test the subprograms instead of whole software program


# check why there is not probability_VI1  ??
# how to add heatmap path-- use relative path for ai product, input path into g.config??
# use django to curl ai server to test it


# 1. load model only one time - test time 
load model: 10- 12s

time for get image:  0.0018551349639892578
Loading models takes 5.888938903808594e-05 seconds
time for prediction: 0.7704911231994629
time for writing in db:  0.013881921768188477
==>time for generatePrediction() in route:  0.8949921131134033 seconds


3. do django to test model ??-- test prediction api
# make the url global visited -- need to under the same network (how to change ip address??)
# how to debug in virtual environment   -- start debug; activate virtual environment; restart debug
5. how to download -- how to upload then can do download; 
6. change prediction post as get --done
8. add report button

heatmap
data
.vscode
*.sqlite3
py37-venv
ai/model_files
__pychache__
