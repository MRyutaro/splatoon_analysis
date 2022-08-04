import cv2
import matplotlib.pyplot as plt
import numpy as np

file = "./data/a.png"
img = cv2.imread(file)

bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
plt.imshow(bgr)
plt.show()

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv_2 = np.copy(hsv)
hsv_3 = np.copy(hsv)

# h>173の画素のhを-90
hsv_2[:, :, 0] = np.where(
    hsv[:, :, 0] > 173, hsv[:, :, 0] - 90, hsv[:, :, 0])  # type: ignore
# h<5の画素のhを+90
hsv_3[:, :, 0] = np.where(
    hsv_2[:, :, 0] < 5, hsv_2[:, :, 0]+90, hsv_2[:, :, 0])  # type: ignore

bgr = cv2.cvtColor(hsv_3, cv2.COLOR_HSV2BGR)

plt.imshow(bgr)
plt.show()
