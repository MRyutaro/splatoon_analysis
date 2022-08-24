import cv2
import time


if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/area_mypinch.mp4')

    frame_count = 0
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))

        my_count = frame[62:85, 322:360]
        your_count = frame[62:85, 408:446]

        # my_pinch
        # cv2.rectangle(frame, (180, 24), (230, 40), (255, 0, 0), 1)
        # cv2.rectangle(frame, (235, 20), (348, 50), (255, 0, 0), 1)
        # cv2.rectangle(frame, (414, 17), (560, 53), (255, 0, 0), 1)

        # your_pinch
        # cv2.rectangle(image, (538, 24), (588, 40), (255, 0, 0), 1)
        # cv2.rectangle(image, (207, 17), (350, 53), (255, 0, 0), 1)
        # cv2.rectangle(image, (418, 21), (533, 50), (255, 0, 0), 1)

        cv2.imshow("image", your_count)
        if cv2.waitKey(1) == 27:
            exit()
        time.sleep(0.03)
        frame_count += 1
