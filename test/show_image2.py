import cv2
import numpy as np


def clip_and_show_image(image, min, max):
    clipped_image = image[min[1]:max[1], min[0]:max[0]]
    print(clipped_image.shape[1], clipped_image.shape[0])
    unique, counts = np.unique(clipped_image, return_counts=True)
    result = np.column_stack((unique, counts))
    print(result)
    cv2.imshow("image", cv2.resize(clipped_image, (10*clipped_image.shape[1], 10*clipped_image.shape[0])))
    cv2.moveWindow("image", 10*clipped_image.shape[1], 10*clipped_image.shape[0])
    # expand_clipped_image = cv2.resize(clipped_image, (10*clipped_image.shape[1], 10*clipped_image.shape[0]))
    # cv2.imwrite('data/image/minute.png', expand_clipped_image)
    if cv2.waitKey(0) == 27:
        exit()


if __name__ == "__main__":
    # image_path = "./data/image/map1.png"
    image_path = "./data/image/5.png"
    image = cv2.imread(image_path)
    image = cv2.resize(image, (768, 432))
    gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray_frame, 100, 255, cv2.THRESH_BINARY)
    image_5 = binary[27:49, 363:380]
    # black
    # clip_and_show_image(image_5, (1, 2), (3, 20))
    # clip_and_show_image(image_5, (1, 2), (16, 3))
    # clip_and_show_image(image_5, (1, 19), (17, 22))
    # clip_and_show_image(image_5, (11, 8), (12, 9))
    # clip_and_show_image(image_5, (4, 12), (6, 13))
    # white
    # clip_and_show_image(image_5, (6, 5), (11, 6))
    # clip_and_show_image(image_5, (5, 6), (7, 9))
    # clip_and_show_image(image_5, (10, 12), (11, 15))
    # clip_and_show_image(image_5, (6, 15), (10, 16))
