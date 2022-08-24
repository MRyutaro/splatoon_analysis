import cv2
import numpy as np


def change_hcolor2white(raw_image, hcolor, hcolor_range):
    # settings
    raw_image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2BGR)
    cmp_color = hcolor-85
    h_lower = int(hcolor-hcolor_range/2)
    h_upper = int(hcolor+hcolor_range/2)
    hsv_lower = np.array([int(h_lower), 0, 0])
    hsv_upper = np.array([int(h_upper), 255, 255])

    # h_binarization
    hsv_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2HSV)
    extracted_image = np.copy(hsv_image)
    extracted_image[:, :, 0] = np.where(extracted_image[:, :, 0] < h_lower,  # type: ignore
                                        cmp_color,
                                        extracted_image[:, :, 0])
    extracted_image[:, :, 0] = np.where(extracted_image[:, :, 0] > h_upper,  # type: ignore
                                        cmp_color,
                                        extracted_image[:, :, 0])

    hsv_mask = cv2.inRange(extracted_image, hsv_lower, hsv_upper)
    masked_image = cv2.bitwise_and(hsv_image, hsv_image, mask=hsv_mask)
    bgr_image = cv2.cvtColor(masked_image, cv2.COLOR_HSV2BGR)
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

    # binarization
    _, binary = cv2.threshold(gray_image, 20, 255, cv2.THRESH_BINARY)
    return binary


if __name__ == "__main__":
    image_path = "./data/image/death2_special1.png"
    # image_path = "./data/image/finish2.png"
    image = cv2.imread(image_path)
    image = cv2.resize(image, (768, 432))
    for i in range(14, 15):
        binary = change_hcolor2white(image, 10*i, 20)
        cv2.imshow(f"{10*i}", binary)
        cv2.moveWindow(f"{10*i}", 700, 300)
        # cv2.imwrite('data/image/finish1_white.jpg', binary)
        cv2.waitKey(0)
