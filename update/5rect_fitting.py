import cv2
import time

movie = cv2.VideoCapture('./data/a.mp4')
# movie = cv2.VideoCapture(1)

x_min, x_max = 200, 356
y_min, y_max = 16, 52

if __name__ == "__main__":
    while True:
        ret, frame = movie.read()

        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))
        detframe = frame[y_min:y_max, x_min:x_max]
        gray = cv2.cvtColor(cv2.bitwise_not(detframe), cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(
            binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > 100, contours))
        # 輪郭位置の補正
        for i in range(len(contours)):
            for j in range(len(contours[i])):
                contours[i][j][0][0] += x_min
                contours[i][j][0][1] += y_min

        for _, cnt in enumerate(contours):
            if len(cnt) > 5:
                x, y, width, height = cv2.boundingRect(cnt)
                print(f"contour: {_}, topleft: ({x}, {y})", end=" ")
                print(f"width: {width}, height: {height}")
                cv2.rectangle(
                    frame, (x, y), (x + width, y + height), (255, 0, 0), 2)

        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 1)

        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        time.sleep(0.024)

    movie.release()
