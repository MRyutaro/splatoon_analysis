import cv2
import numpy as np


if __name__ == "__main__":
    image_path = "./data/image/map1.png"
    # image_path = "./data/image/5.png"
    image = cv2.imread(image_path)
    image = cv2.resize(image, (768, 432))
    clipped_image = image[29:47, 365:401]
    cv2.imshow("image", clipped_image)
    if cv2.waitKey(0) == 27:
        exit()
