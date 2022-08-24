import cv2
import numpy as np
import time


def check_finish_game(frame):
    finish_range = [["upper_left", [35, 43], [87, 68], 255],
                    ["upper_right", [549, 28], [581, 41], 255],
                    ["botton_left", [29, 282], [154, 298], 255],
                    ["bottom_right", [508, 364], [610, 383], 255]]
    binary = change_color2white(frame, 140, 30)
    for i in range(len(finish_range)):
        if check_whether_one_color(
                binary, finish_range[i][1], finish_range[i][2], finish_range[i][3]) is False:
            return True
    return False


def change_color2white(raw_image, color, color_range):
    # settings
    raw_image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2BGR)
    cmp_color = color-85
    h_lower = int(color-color_range/2)
    h_upper = int(color+color_range/2)
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


def check_whether_one_color(binary, min, max, color):
    clipped_range = binary[min[1]:max[1], min[0]:max[0]]
    unique, counts = np.unique(clipped_range, return_counts=True)
    result = np.column_stack((unique, counts))
    if len(result) == 1:
        if result[0][0] == color:
            return True
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    # movie = cv2.VideoCapture(1)
    movie = cv2.VideoCapture('./data/video/asari_trim3.mp4')

    is_gaming = True
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))

        if is_gaming is True:
            is_gaming = check_finish_game(frame)
        print(is_gaming)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.02)

    movie.release()
