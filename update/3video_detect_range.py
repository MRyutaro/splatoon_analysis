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

        # BGR -> grayscale
        gray = cv2.cvtColor(cv2.bitwise_not(detframe), cv2.COLOR_BGR2GRAY)

        # 閾値処理
        _, binary = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)

        #  輪郭抽出
        contours, _ = cv2.findContours(
            binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours = list(filter(lambda x: cv2.contourArea(x) > 500, contours))
        # 輪郭位置の補正
        for i in range(len(contours)):
            for j in range(len(contours[i])):
                contours[i][j][0][0] += x_min
                contours[i][j][0][1] += y_min

        cv2.drawContours(frame, contours, -1, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 1)

        cv2.imshow('frame', cv2.resize(frame, (int(768), int(432))))
        cv2.waitKey(1)
        time.sleep(0.024)

    # 撮影用オブジェクトとウィンドウの解放
    movie.release()
