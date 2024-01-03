from roboflow import Roboflow

import time

start =  time.time()


rf = Roboflow(api_key="AANXuvM9YlfNPlUimt66")
project = rf.workspace().project("people-detection-general")
model = project.version(7).model

# infer on a local image
prediction = model.predict("group.jpg", confidence=40, overlap=30).json()

print(len(prediction['predictions']))


end = time.time()

print(end - start)