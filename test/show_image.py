import cv2
import numpy as np

image_path = "./data/image/map1.png"
# image_path = "./data/image/5.png"
image = cv2.imread(image_path)
image = cv2.resize(image, (768, 432))
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray_frame, 50, 255, cv2.THRESH_BINARY)
cv2.imshow("x_icon", binary)
cv2.waitKey(0)

# x_icon = binary[35:55, 45:65]
# unique, counts = np.unique(x_icon, return_counts=True)
# result = np.column_stack((unique, counts))
# if 125 < result[0][1] < 145:
#     if 255 < result[1][1] < 275:
#         print(1)
# print("x_icon-----------\n", result)
# cv2.imshow("x_icon", x_icon)
# cv2.waitKey(0)


down_button_icon = binary[374:404, 300:465]
unique, counts = np.unique(down_button_icon, return_counts=True)
result = np.column_stack((unique, counts))
print("down_button_icon-----------\n", result)
cv2.imshow("down_button_icon", down_button_icon)
cv2.waitKey(0)
