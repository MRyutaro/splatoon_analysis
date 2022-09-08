import cv2

image_path = "./data/image/my_pinch.png"
image = cv2.imread(image_path)
image = cv2.resize(image, (768, 432))
# gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# _, binary = cv2.threshold(gray_frame, 100, 255, cv2.THRESH_BINARY)
cv2.imshow("image", image)
if cv2.waitKey(0) == 27:
    exit()
