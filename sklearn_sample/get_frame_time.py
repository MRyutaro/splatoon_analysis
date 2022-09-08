import cv2
import json
import time
import toml


def main():
    open_position = open('config/json/position.json', 'r')
    position = json.load(open_position)

    movie = cv2.VideoCapture(capture_mode_setting())
    frame_width, frame_height = position["frame_size"]["width"], position["frame_size"]["height"]

    frame_count = 0
    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (frame_width, frame_height))

        # num_image1 = frame[30:45, 366:375]
        # cv2.imwrite(
        #     f'data/num_dataset/train/minute/{frame_count}.png', num_image1)
        # cv2.rectangle(frame, (382, 30), (391, 45), (255, 0, 0), 1)
        # num_image2 = frame[30:45, 382:391]
        # cv2.imwrite(
        #     f'data/num_dataset/train/tens/{frame_count}.png', num_image2)
        # cv2.rectangle(frame, (391, 30), (400, 45), (255, 0, 0), 1)
        # num_image3 = frame[30:45, 391:400]
        # cv2.imwrite(
        #     f'data/num_dataset/train/ones/{frame_count}.png', num_image3)
        # cv2.imwrite(
        #     f'data/image/pinch/enemy/{frame_count}.png', frame)

        cv2.imshow('frame', cv2.resize(frame, (960, 540)))
        if cv2.waitKey(1) == 27:
            exit()

        if frame_count > 10:
            break
        print(frame_count)
        frame_count += 1
        # time.sleep(0.05)

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


if __name__ == "__main__":
    main()
