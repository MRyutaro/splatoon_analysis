import cv2
import matplotlib.pyplot as plt

# 入力ファイルのパスを指定
file = "./data/sample.png"

# 読み込み
image = cv2.imread(file)
image = cv2.resize(image, (768, 432))
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

x_min, x_max = 216, 356
y_min, y_max = 16, 52


if __name__ == "__main__":
    image_copy1 = image[y_min:y_max, x_min:x_max]
    # グレースケール化
    image_copy1 = cv2.cvtColor(image_copy1, cv2.COLOR_BGR2GRAY)
    # 閾値処理
    ret, thresh = cv2.threshold(image_copy1, 95, 255, cv2.THRESH_BINARY)

    # 輪郭検出
    contours1, hierarchy1 = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 輪郭位置の補正
    for i in range(len(contours1)):
        for j in range(len(contours1[i])):
            contours1[i][j][0][0] += x_min
            contours1[i][j][0][1] += y_min

    # 結果の描画
    cv2.drawContours(image, contours1, -1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

    plt.imshow(image)
    plt.show()
