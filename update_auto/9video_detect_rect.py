import cv2
import numpy as np
from time import sleep
import toml


def main():
    obj = toml.load("settings.toml")
    select_mode = obj["setting"]["MODE"]
    capture_content = 1
    if select_mode == "recorded":
        capture_content = obj["setting"]["VIDEO_PATH"]
    elif select_mode == "live":
        capture_content = obj["setting"]["PORT_NUM"]
    else:
        print("ERROR")
        exit()
    movie = cv2.VideoCapture(capture_content)
    movie_width = 768
    movie_height = 432

    frame_size_rate = obj["image_setting"]["SIZE_RATE"]
    sleep_time = obj["video_setting"]["SLEEP_TIME"]
    # image settings--------------
    min_x, min_y = int(200*frame_size_rate), int(16*frame_size_rate)
    max_x, max_y = int(356*frame_size_rate), int(52*frame_size_rate)
    clipped_range = [[min_x, min_y], [max_x, max_y]]

    icon_area_lower = int(200*frame_size_rate)
    icon_area_upper = int(3000*frame_size_rate)

    resize_x = int(movie_width*frame_size_rate)
    resize_y = int(movie_height*frame_size_rate)

    # color settings--------------
    ink_color = 170
    color_range = 10

    squareness_valid_range = 0.2
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (resize_x, resize_y))

        binary_image = change_color2white(frame, ink_color, color_range)
        contours = extract_contours(binary_image, clipped_range, 5)
        binary_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2RGB)

        # 短径フィッティング
        # for i, cnt in enumerate(contours):
            # if len(cnt) > 5:
            #     center, (width, height), angle = cv2.fitEllipse(cnt)
            #     cv2.putText(binary_image, str(i), (int(center[0]), int(center[1])), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1, cv2.LINE_AA)
            #     cv2.ellipse(binary_image, ((center[0], center[1]), (width, height), angle), (255, 0, 0))  # type: ignore
            # x, y, width, height = cv2.boundingRect(cnt)
            # area = width*height
            # if icon_area_lower < area < icon_area_upper:
            #     # if 1-squareness_valid_range < height/width < 1+squareness_valid_range:
            #     cv2.rectangle(
            #         frame, (x, y), (x + width, y + height), (255, 0, 0), 1)
            #     cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_PLAIN,
            #                 1, (0, 255, 0), 1, cv2.LINE_AA)

        cv2.drawContours(frame, contours, -1,
                         (0, 0, 255), -1, cv2.LINE_AA)
        # cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 1)

        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        sleep(sleep_time)

    movie.release()


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


if __name__ == "__main__":
    main()
