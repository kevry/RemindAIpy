import cv2
import os
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf

class Classifier():
	def __init__(self):
		self.model = tf.keras.models.load_model("model_resnet1", compile=False)

	def run_inference(self, frame):
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frame = cv2.resize(frame, (224,224))
		predictions = self.model.predict(np.array([frame]))
		pred_idx = np.argmax(predictions)
		return pred_idx