import cv2
import matplotlib.pyplot as plt
import numpy as np

file = "./data/image/a.png"
img = cv2.imread(file)
bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

fig = plt.figure()
X = 2
Y = 2

# imgの表示
imgplot = 1
ax1 = fig.add_subplot(X, Y, imgplot)
ax1.set_title("raw-image", fontsize=10)
plt.imshow(bgr)

hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
hsv_2 = np.copy(hsv)

color = 170
cmp_color = color-85
# cmp_color = 170
hsv_2[:, :, 0] = np.where(hsv[:, :, 0] < color-5, cmp_color,  # type: ignore
                          hsv[:, :, 0])
hsv_2[:, :, 0] = np.where(hsv_2[:, :, 0] > color+5, cmp_color,  # type: ignore
                          hsv_2[:, :, 0])

hsv_lower = np.array([int(color-10), 0, 0])
hsv_upper = np.array([int(color+10), 255, 255])
hsv_mask = cv2.inRange(hsv_2, hsv_lower, hsv_upper)
masked_hsv_2 = cv2.bitwise_and(hsv, hsv, mask=hsv_mask)
masked_bgr_2 = cv2.cvtColor(masked_hsv_2, cv2.COLOR_HSV2BGR)

bgr_2 = cv2.cvtColor(masked_bgr_2, cv2.COLOR_BGR2GRAY)

# 閾値処理
_, binary = cv2.threshold(bgr_2, 20, 255, cv2.THRESH_BINARY)

# img2の表示
img2plot = 2
ax2 = fig.add_subplot(X, Y, img2plot)
ax2.set_title("インクの色を際立たせる", fontsize=10)
plt.imshow(cv2.cvtColor(hsv_2, cv2.COLOR_HSV2BGR))

# img3の表示
img2plot = 3
ax2 = fig.add_subplot(X, Y, img2plot)
ax2.set_title("抽出後", fontsize=10)
plt.imshow(masked_bgr_2)

# img4の表示
img2plot = 4
ax2 = fig.add_subplot(X, Y, img2plot)
ax2.set_title("白黒", fontsize=10)
plt.imshow(binary, cmap="gray")
plt.show()
