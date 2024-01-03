import joblib 
import time

start = time.time()

model = joblib.load('model.pkl')
prediction = model.predict("group.jpg", confidence=40, overlap=30).json()
print(len(prediction['predictions']))

end = time.time()

print(f"Execution Time - {end-start}")