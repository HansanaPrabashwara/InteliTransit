import joblib 
import time
import cv2

start = time.time()

img = cv2.imread('group3.png')


model = joblib.load('model.pkl')
prediction = model.predict("group3.png", confidence=40, overlap=30).json()
print(len(prediction['predictions']))

for i in prediction['predictions']:
    print(i)
    img = cv2.rectangle(img, (int(i['x']-i['width']/2), int(i['y']-i['height']/2)), (int(i['x']+i['width']/2), int(i['y']+i['height']/2)), (0, 255, 0), 2)

cv2.imshow('detcted faces',img)
end = time.time()

print(f"Execution Time - {end-start}")

cv2.waitKey(0)