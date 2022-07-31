#
# 色抽出のサンプルコード
#
import numpy as np
import cv2
from time import sleep


# メイン関数
def main():
    image = cv2.imread('./data/sample.png')  # ファイル読み込み
    height = image.shape[0]
    width = image.shape[1]
    image = cv2.resize(image, (round(width/4), round(height/4)))

    # BGRでの色抽出
    bgrLower = np.array([0, 0, 0])    # 抽出する色の下限
    bgrUpper = np.array([70, 235, 255])    # 抽出する色の上限
    bgrResult = bgrExtraction(image, bgrLower, bgrUpper)
    cv2.imshow('BGR_test1', bgrResult)
    sleep(1)

    # HSVでの色抽出
    # hsvLower = np.array([30, 153, 255])    # 抽出する色の下限
    # hsvUpper = np.array([30, 153, 255])    # 抽出する色の上限
    # hsvResult = hsvExtraction(image, hsvLower, hsvUpper)
    # cv2.imshow('HSV_test1', hsvResult)
    # sleep(1)

    cv2.destroyAllWindows()


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
