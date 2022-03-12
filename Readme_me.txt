Steps to run AI server based on python3.7
vir  # create virtual env python3.7
pip install -r requirements.txt
mkdir ai/model_files ## then add 3 model files into this folder 
set FLASK_APP=manager

python -m flask db init  # create db.sqlite
python -m flask db migrate -m "init" 
python -m flask db upgrade
python -m flask forge  #create fake 20 images 



# Setting on AI 
samples: 20 images is downloaded from kaggle dataset; the other 5 images are from Retina camera

Time for running AI server 
10s: load all models 
on AI model: 
1-2s: get prediction per image




    # print('request.headers', dict(request.headers))
#{'Host': '192.168.50.170:5050', 'User-Agent': 'python-requests/2.27.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', \
    # 'Connection': 'keep-alive', 'Content-Type': 'application/json', 'Content-Length': '1738033'}
