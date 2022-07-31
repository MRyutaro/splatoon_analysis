import cv2
import numpy as np

# ファイル読み込み
image = cv2.imread('./data/sample.png')

# BGRでの色抽出
# 抽出する色の下限(BGR)
bgrLower = np.array([102, 255, 255])
# 抽出する色の上限(BGR)
bgrUpper = np.array([102, 255, 255])
# BGRからマスクを作成
img_mask = cv2.inRange(image, bgrLower, bgrUpper)
# 元画像とマスクを合成
result = cv2.bitwise_and(image, image, mask=img_mask)
