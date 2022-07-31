import cv2
import matplotlib.pyplot as plt

# 入力ファイルのパスを指定
file = "./data/a.png"

# 認識範囲
xmin, xmax = 540, 890
ymin, ymax = 40, 130

# 読み込み
image = cv2.imread(file)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 画像のサイズ縮小
# height = image.shape[0]
# width = image.shape[1]
# image = cv2.resize(image,(round(width/4), round(height/4)))

image_copy1 = image[ymin:ymax, xmin:xmax]
# グレースケール化
image_copy1 = cv2.cvtColor(image_copy1, cv2.COLOR_BGR2GRAY)

# 閾値処理
ret, thresh = cv2.threshold(image_copy1, 95, 255, cv2.THRESH_BINARY)

# 輪郭検出 （cv2.ChAIN_APPROX_SIMPLE）
contours1, hierarchy1 = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 輪郭の描画
# contours1[0] += xmin
# contours1[1] += ymin
print(len(contours1))
for i in range(len(contours1)):
    print(contours1[i][0][0])
    print(contours1[i][0][1])

cv2.drawContours(image, contours1, -1, (0, 255, 0), 2, cv2.LINE_AA)

# 認識範囲に赤枠
cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

# 入力画像の表示
plt.imshow(image)
plt.show()
