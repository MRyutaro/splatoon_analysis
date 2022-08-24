import cv2
import matplotlib.pyplot as plt
import numpy as np

# 入力ファイルのパスを指定
file = "./data/image/a.png"

# 読み込み
image = cv2.imread(file)
image = cv2.resize(image, (768, 432))
image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

x_min, x_max = 200, 356
y_min, y_max = 16, 52

hsv_lower = np.array([65, 0, 0])
hsv_upper = np.array([85, 255, 255])


# HSVで特定の色を抽出する関数
def hsvExtraction(image, hsvLower, hsvUpper):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)
    result = cv2.bitwise_and(image, image, mask=hsv_mask)
    return result


if __name__ == "__main__":
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_HSV2BGR))
    # plt.show()
    image_color_mask = hsvExtraction(image, hsv_lower, hsv_upper)
    plt.imshow(cv2.cvtColor(image_color_mask, cv2.COLOR_HSV2BGR))
    plt.show()
    # グレースケール化
    gray_image = np.copy(image)
    gray_image[:, :, 0] = np.where(
        image[:, :, 0] > hsv_upper[0],
        image[:, :, 0] - 90, image[:, :, 0])  # type: ignore
    plt.imshow(cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR))
    plt.show()
    # 閾値処理
    ret, thresh = cv2.threshold(gray_image, 40, 255, cv2.THRESH_BINARY)
    plt.imshow(cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR))
    plt.show()
