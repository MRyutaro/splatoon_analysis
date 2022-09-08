import cv2
import json
import matplotlib.pyplot as plt
import numpy as np
from time import sleep
import toml


def main():
    open_position = open('config/position.json', 'r')
    position = json.load(open_position)
    open_color = open('config/color.json', 'r')
    color = json.load(open_color)

    movie = cv2.VideoCapture(capture_mode_setting())
    frame_width, frame_height = position["frame_size"]["width"], position["frame_size"]["height"]
    my_icon_range = [[position["icon"]["my"]["min"]["x"],
                      position["icon"]["my"]["min"]["y"]],
                     [position["icon"]["my"]["max"]["x"],
                     position["icon"]["my"]["max"]["y"]]]

    ink_color = color["purple"]["hue"]
    color_range = color["purple"]["range"]

    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (frame_width, frame_height))

        binary_image = change_color2white(frame, ink_color, color_range)

        contours = extract_contours(binary_image, my_icon_range, 10)
        # contours = list(
        #     map(lambda x: cv2.approxPolyDP(x, 12, False), contours))
        # for i, cnt in enumerate(contours):
        #     x, y, width, height = cv2.boundingRect(cnt)

        #     cv2.rectangle(
        #         frame, (x, y), (x + width, y + height), (255, 0, 0), 1)
        #     cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_PLAIN,
        #                 1, (0, 255, 0), 1, cv2.LINE_AA)

        cv2.drawContours(frame, contours, -1, (0, 0, 255), 0, cv2.LINE_AA)

        cv2.imshow('frame', cv2.resize(frame, (1920, 1080)))
        cv2.waitKey(1)
        sleep(0.05)

    movie.release()


def capture_mode_setting():
    obj = toml.load("config/settings.toml")
    select_mode = obj["setting"]["MODE"]
    capture_content = 1
    if select_mode == "recorded":
        capture_content = obj["setting"]["VIDEO_PATH"]
    elif select_mode == "live":
        capture_content = obj["setting"]["PORT_NUM"]
    else:
        print("ERROR at settings.toml.")
        exit()
    return capture_content


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


def extract_contours(binary_image, clipped_range, contours_area_lower):
    clipped_frame = binary_image[clipped_range[0][1]:clipped_range[1][1],
                                 clipped_range[0][0]:clipped_range[1][0]]
    dst = cv2.adaptiveThreshold(
        clipped_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 50)

    plt.imshow(clipped_frame, cmap="gray")
    plt.show()

    # 輪郭抽出
    contours, _ = cv2.findContours(
        dst, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # フィルタ
    contours = list(filter(lambda x: cv2.contourArea(x)
                    > contours_area_lower, contours))

    # 輪郭位置の補正
    for i in range(len(contours)):
        for j in range(len(contours[i])):
            contours[i][j][0][0] += clipped_range[0][0]
            contours[i][j][0][1] += clipped_range[0][1]
    return contours


if __name__ == "__main__":
    main()
