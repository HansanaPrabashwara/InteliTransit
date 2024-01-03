import json
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename 
import joblib
from datetime import datetime
import time
import os
import cv2
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['PROCESSED_FOLDER'] = os.path.join('static','processed')

model = joblib.load('model.pkl')



@app.route('/')
def home():
    return render_template('home.html', image = latest_image_path)


@app.route('/solution')
def solution():
    return render_template('solution.html')


@app.route('/implementation')
def implementation():
    return render_template('implementation.html')


@app.route('/contributors')
def contributors():
    return render_template('contributors.html')

@app.route('/cv')
def cv():

    all_image_data = pd.read_csv("log.csv")
    latest_image_data = all_image_data.iloc[-1]
    
    prediction = joblib.load('prediction.pkl')

    img = cv2.imread(latest_image_data['path'])
    
    for i in prediction['predictions']:
        img = cv2.rectangle(img, (int(i['x']-i['width']/2), int(i['y']-i['height']/2)), (int(i['x']+i['width']/2), int(i['y']+i['height']/2)), (255, 0, 0), 1)
        cv2.putText(img, 'Person', (int(i['x']-i['width']/2), int(i['y']-i['height']/2)), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,0,0), 1,1,)


    cv2.imwrite(os.path.join(app.config['PROCESSED_FOLDER'], latest_image_data['name']),img)

    return render_template('cv.html', image = os.path.join(app.config['PROCESSED_FOLDER'], latest_image_data['name']),
                           name = latest_image_data['name'], count = latest_image_data['count'], 
                           predictions = prediction['predictions'], upload_time = latest_image_data['timestamp'], 
                           refresh_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S"))




@app.route('/cv', methods=['POST'])
def count_people_endpoint():
    file = request.files['image']
    file_name = datetime.now().strftime("%Y%m%d%H%M%S") + secure_filename(file.filename)
    # file.save(file_name)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
    
    
    
    # image = load_and_preprocess_image(file.read())
    start = time.time()
    prediction = model.predict(os.path.join(app.config['UPLOAD_FOLDER'], file_name), confidence=40, overlap=30).json()
    people_count = len(prediction['predictions'])

    
    # Add data to the log file

    image_data = [{
        'timestamp': datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
        'name': file_name, 
        'path': os.path.join(app.config['UPLOAD_FOLDER'], file_name), 
        'count':  len(prediction['predictions'])
        }]

    df = pd.DataFrame(image_data)

    df.to_csv('log.csv', mode="a")

    joblib.dump(prediction,'prediction.pkl')


    end = time.time()
    return jsonify({'people_count': people_count,
                    'execution_time':end-start})







