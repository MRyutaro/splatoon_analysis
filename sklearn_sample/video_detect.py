import cv2
import numpy as np
import tensorflow as tf
import time


def check_is_gaming(frame):
    model = tf.keras.models.load_model(
        './sklearn_sample/data/model/my_model.h5')
    minute = frame[30:45, 366:375]
    image = np.array(minute) / 255
    image_expand = image[np.newaxis, ...]
    predictions_single = model.predict(image_expand)
    print(predictions_single[0])
    max_probability_num = np.amax(predictions_single[0])
    if max_probability_num > 0.6:
        print(predictions_single[0].argmax())
        print(predictions_single[0].argmin())
        if predictions_single[0].argmax() == 5:
            return True
    return False


if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/asari.mp4')

    is_gaming = False
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))

        if is_gaming is False:
            is_gaming = check_is_gaming(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.rectangle(frame, (366, 30), (375, 45), (255, 0, 0), 1)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

    movie.release()
