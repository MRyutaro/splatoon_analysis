import tensorflow as tf
import cv2
import numpy as np


model = tf.keras.models.load_model('./sklearn_sample/data/model/my_model.h5')

image_path = "./sklearn_sample/data/raw_data/5.jpg"
image = cv2.imread(image_path)
image = np.array(image)/255
image_expand = image[np.newaxis, ...]
# print(image_expand.shape)

predictions_single = model.predict(image_expand)
max_probability_num = np.amax(predictions_single)
if max_probability_num > 0.6:
    print(predictions_single[0].argmax())
