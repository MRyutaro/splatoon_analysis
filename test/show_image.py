import cv2
import numpy as np
import statistics


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
    image_path = "./data/image/death2_special1.png"
    # image_path = "./data/image/1.png"
    image = cv2.imread(image_path)
    image = cv2.resize(image, (768, 432))
    bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    # _, binary = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)
    clipped_image_1 = hsv_image[22:48, 247:273]
    cv2.imshow("image", clipped_image_1)
    S_mode_1 = statistics.mode(clipped_image_1[:, :, 2].flatten())
    print("player1 v =", S_mode_1)
    clipped_image_3 = image[22:48, 322:348]
    S_mode_3 = statistics.mode(clipped_image_3[:, :, 2].flatten())
    print("player3 v =", S_mode_3)

    # unique1, counts1 = np.unique(clipped_image_death, return_counts=True)
    # unique2, counts2 = np.unique(clipped_image_sp, return_counts=True)

    # result1 = np.column_stack((unique1, counts1))
    # result2 = np.column_stack((unique2, counts2))

    cv2.rectangle(image, (247, 22), (273, 48), (255, 0, 0), 1)
    cv2.rectangle(image, (322, 22), (348, 48), (255, 0, 0), 1)

    # print("death", result1)
    # print("sp", result2)

    cv2.imshow("image", image)
    if cv2.waitKey(0) == 27:
        exit()

    # _, binary = cv2.threshold(gray_frame, 150, 255, cv2.THRESH_BINARY)
    # count = 0
    # count = show_clipped(binary, "binary", (0, 0), (768, 432), count)
    # count = show_clipped(binary, "left", (45, 205), (50, 222), count)
    # count = show_clipped(binary, "top", (309, 40), (329, 44), count)
    # count = show_clipped(binary, "right", (587, 204), (591, 225), count)
    # count = show_clipped(binary, "down", (309, 385), (329, 390), count)
    # print(count)
