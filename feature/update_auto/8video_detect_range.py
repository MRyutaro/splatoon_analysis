import cv2
import numpy as np
import time

movie = cv2.VideoCapture('./data/video/asari.mp4')
# movie = cv2.VideoCapture(1)

x_min, x_max = 200, 356
y_min, y_max = 16, 52

ink_color = 170
cmp_color = ink_color-85
h_lower = ink_color-10
h_upper = ink_color+10

hsv_lower = np.array([int(h_lower), 0, 0])
hsv_upper = np.array([int(h_upper), 255, 255])


if __name__ == "__main__":
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        detframe = frame[y_min:y_max, x_min:x_max]

        # BGR -> grayscale
        detframe = cv2.cvtColor(detframe, cv2.COLOR_BGR2HSV)
        copy_detframe = np.copy(detframe)
        copy_detframe[:, :, 0] = np.where(detframe[:, :, 0] < h_lower,  # type: ignore
                                          cmp_color,
                                          detframe[:, :, 0])
        copy_detframe[:, :, 0] = np.where(copy_detframe[:, :, 0] > h_upper,  # type: ignore
                                          cmp_color,
                                          copy_detframe[:, :, 0])
        hsv_mask = cv2.inRange(copy_detframe, hsv_lower, hsv_upper)
        masked_detframe = cv2.bitwise_and(detframe, detframe, mask=hsv_mask)
        detframe = cv2.cvtColor(masked_detframe, cv2.COLOR_HSV2BGR)
        detframe = cv2.cvtColor(detframe, cv2.COLOR_BGR2GRAY)

        # 閾値処理
        _, binary = cv2.threshold(detframe, 20, 255, cv2.THRESH_BINARY)

        #  輪郭抽出
        contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 面積でフィルタ
        contours = list(filter(lambda x: cv2.contourArea(x) > 500, contours))
        # 輪郭位置の補正
        for i in range(len(contours)):
            for j in range(len(contours[i])):
                contours[i][j][0][0] += x_min
                contours[i][j][0][1] += y_min

        cv2.drawContours(frame, contours, -1, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 1)

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('frame', cv2.resize(frame, (int(768), int(432))))
        cv2.waitKey(1)
        time.sleep(0.024)

    # 撮影用オブジェクトとウィンドウの解放
    movie.release()
