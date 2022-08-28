import cv2
import time
import numpy as np


if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/pinch/area_mypinch_only.mp4')
    # movie = cv2.VideoCapture('./data/video/pinch/area_yourpinch_only.mp4')

    frame_count = 0
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))

        # count_range
        # my_count = frame[62:85, 322:360]
        # your_count = frame[62:85, 408:446]

        # pinch_range
        my_pinch_range = frame[27:40, 184:226]
        your_pinch_range = frame[27:40, 542:581]

        # my_pinch
        # cv2.rectangle(frame, (180, 24), (230, 40), (255, 0, 0), 1)
        # cv2.rectangle(frame, (235, 20), (348, 50), (255, 0, 0), 1)
        # cv2.rectangle(frame, (414, 17), (560, 53), (255, 0, 0), 1)

        # your_pinch
        # cv2.rectangle(image, (538, 24), (588, 40), (255, 0, 0), 1)
        # cv2.rectangle(image, (207, 17), (350, 53), (255, 0, 0), 1)
        # cv2.rectangle(image, (418, 21), (533, 50), (255, 0, 0), 1)

        # 色変換
        my_pinch_range_hsv = cv2.cvtColor(my_pinch_range, cv2.COLOR_BGR2HSV)
        my_pinch_range_color = [my_pinch_range_hsv[:, :, 0],
                                my_pinch_range_hsv[:, :, 1],
                                my_pinch_range_hsv[:, :, 2]]
        my_pinch_range_color_mean = [np.mean(my_pinch_range_color[0]),
                                     np.mean(my_pinch_range_color[1]),
                                     np.mean(my_pinch_range_color[2])]
        print(my_pinch_range_color_mean)

        cv2.imshow("image", my_pinch_range)
        if cv2.waitKey(1) == 27:
            exit()
        time.sleep(0.03)
        frame_count += 1
