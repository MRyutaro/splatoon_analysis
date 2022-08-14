import cv2
import numpy as np


def show_clipped(binary, icon_name, min, max, count):
    clipped_range = binary[min[1]:max[1], min[0]:max[0]]
    unique, counts = np.unique(clipped_range, return_counts=True)
    result = np.column_stack((unique, counts))
    # print(icon_name, "\n", result)
    # cv2.imshow(icon_name, clipped_range)
    # if cv2.waitKey(0) == 27:
    #     exit()
    if len(result) == 1:
        if result[0][0] == 255:
            return count + 1
    else:
        return count


if __name__ == "__main__":
    image_path = "./data/image/map1.png"
    # image_path = "./data/image/5.png"
    image = cv2.imread(image_path)
    image = cv2.resize(image, (768, 432))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)
    count = 0
    count = show_clipped(binary, "binary", (0, 0), (768, 432), count)
    count = show_clipped(binary, "left", (45, 205), (50, 222), count)
    count = show_clipped(binary, "top", (309, 40), (329, 44), count)
    count = show_clipped(binary, "right", (587, 204), (591, 225), count)
    count = show_clipped(binary, "down", (309, 385), (329, 390), count)
    print(count)
