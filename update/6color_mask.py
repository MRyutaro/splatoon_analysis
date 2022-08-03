import numpy as np
import cv2
import time


movie = cv2.VideoCapture('./data/a.mp4')
# movie = cv2.VideoCapture(0)

x_min, x_max = 200, 356
y_min, y_max = 16, 52

bgrLower = np.array([0, 0, 0])    # 抽出する色の下限
bgrUpper = np.array([255, 100, 240])    # 抽出する色の上限


def main():
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))

        # BGRでの色抽出
        bgrResult = bgrExtraction(frame, bgrLower, bgrUpper)
        cv2.imshow('BGR_test1', bgrResult)
        cv2.waitKey(1)
        time.sleep(0.024)

    movie.release()


# BGRで特定の色を抽出する関数
def bgrExtraction(image, bgrLower, bgrUpper):
    img_mask = cv2.inRange(image, bgrLower, bgrUpper)  # BGRからマスクを作成
    result = cv2.bitwise_and(image, image, mask=img_mask)  # 元画像とマスクを合成
    return result


# HSVで特定の色を抽出する関数
def hsvExtraction(image, hsvLower, hsvUpper):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # 画像をHSVに変換
    hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)    # HSVからマスクを作成
    result = cv2.bitwise_and(image, image, mask=hsv_mask)  # 元画像とマスクを合成
    return result


if __name__ == '__main__':
    main()
