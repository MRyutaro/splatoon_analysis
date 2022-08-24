import cv2
import matplotlib.pyplot as plt
import numpy as np

file = "./data/a.png"
img = cv2.imread(file)

fig = plt.figure()
X = 2
Y = 2

bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
# imgの表示
imgplot = 1
ax1 = fig.add_subplot(X, Y, imgplot)
# タイトルの設定
ax1.set_title("raw-image", fontsize=20)
plt.imshow(bgr)

hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
hsv_2 = np.copy(hsv)
hsv_3 = np.copy(hsv)

# h>173の画素のhを-90
hsv_2[:, :, 0] = np.where(
    hsv[:, :, 0] > 173, hsv[:, :, 0] - 90, hsv[:, :, 0])  # type: ignore
# h<5の画素のhを+90
hsv_3[:, :, 0] = np.where(
    hsv_2[:, :, 0] < 5, hsv_2[:, :, 0]+90, hsv_2[:, :, 0])  # type: ignore

bgr2 = cv2.cvtColor(hsv_3, cv2.COLOR_HSV2BGR)

# img2の表示
img2plot = 4
ax2 = fig.add_subplot(X, Y, img2plot)
# タイトルの設定
ax2.set_title("change-color-image", fontsize=20)
plt.imshow(bgr2)
plt.show()
