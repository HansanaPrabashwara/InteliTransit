from roboflow import Roboflow

import joblib 

rf = Roboflow(api_key="AANXuvM9YlfNPlUimt66")
project = rf.workspace().project("people-detection-general")
model = project.version(7).model

joblib.dump(model,'model.pkl')

# infer on a local image
prediction = model.predict("group2.jpg", confidence=40, overlap=30).json()

print(len(prediction['predictions']))