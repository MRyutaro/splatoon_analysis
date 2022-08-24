import cv2


def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


# path = "data/image/band/my_band_in_your_pinch.png"
path = "data/image/band/your_band_in_my_pinch.png"
img = cv2.imread(path)
# print(img.shape)
cv2.imshow('sample', img)
cv2.setMouseCallback('sample', onMouse)
cv2.waitKey(0)
