import cv2

# 入力ファイルのパスを指定
file = "./data/image/5.png"

# 読み込み
image = cv2.imread(file)
image = cv2.resize(image, (768, 432))

x_min, x_max = 365, 375
y_min, y_max = 29, 45

cut_copy = image[y_min:y_max, x_min:x_max]

cv2.imwrite('./data/image/cut5.png', cut_copy)
