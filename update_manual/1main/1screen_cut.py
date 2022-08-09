import cv2
import numpy as np
import toml
from time import sleep


obj = toml.load("settings.toml")
select_mode = obj["setting"]["MODE"]
capture_content = 1
if select_mode == "recorded":
    capture_content = obj["setting"]["VIDEO_PATH"]
elif select_mode == "live":
    capture_content = obj["setting"]["PORT_NUM"]
else:
    print("ERROR occurs at settings.toml.")
    exit()
movie = cv2.VideoCapture(capture_content)

frame_size_rate = obj["image_setting"]["SIZE_RATE"]
sleep_time = obj["video_setting"]["SLEEP_TIME"]


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
    min_x, min_y = clipped_range[0][:]
    max_x, max_y = clipped_range[1][:]
    detframe = binary_image[min_y:max_y, min_x:max_x]
    # 輪郭抽出
    contours, _ = cv2.findContours(
        detframe, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # フィルタ
    contours = list(filter(lambda x: cv2.contourArea(x)
                    > contours_area_lower, contours))
    # contours = list(map(lambda x: cv2.approxPolyDP(x, 1, True), contours))
    # 輪郭位置の補正
    for i in range(len(contours)):
        for j in range(len(contours[i])):
            contours[i][j][0][0] += min_x
            contours[i][j][0][1] += min_y
    return contours


if __name__ == '__main__':
    my_x_min, my_x_max = 200, 356
    my_y_min, my_y_max = 16, 52
    your_x_min, your_x_max = 568, 412
    your_y_min, your_y_max = 16, 52
    area_lower = 150

    while True:
        ret, frame = movie.read()
        frame = cv2.resize(frame, (768, 432))
        if ret is None:
            break

        binary = change_color2white(frame, 170, 10)
        dst = cv2.adaptiveThreshold(
            binary, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 40)
        contours = extract_contours(binary, [[200, 16], [356, 52]], 10)

        # if len(contours) > 0:
        for i, cnt in enumerate(contours):
            x, y, width, height = cv2.boundingRect(cnt)
            area = width*height
            if area > area_lower:
                cv2.rectangle(
                    frame, (x, y), (x + width, y + height), (255, 0, 0), 1)
                cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_PLAIN,
                            1, (0, 255, 0), 1, cv2.LINE_AA)

        # cv2.rectangle(
        #     frame, (my_x_min, my_y_min), (my_x_max, my_y_max), (255, 0, 0), 1)
        # cv2.rectangle(
        #     frame, (your_x_min, your_y_min), (your_x_max, your_y_max), (255, 0, 0), 1)

        cv2.imshow('frame', cv2.resize(frame, (1920, 1080)))
        cv2.waitKey(1)
        sleep(sleep_time)
    movie.release()
