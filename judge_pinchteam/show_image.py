import cv2


if __name__ == "__main__":
    image_path = "./data/image/friend_pinch.png"
    # image_path = "./data/image/enemy_pinch.png"
    # image_path = "./data/image/5.png"
    image = cv2.imread(image_path)
    image = cv2.resize(image, (768, 432))

    my_range = image[39:47, 207:350]
    your_range = image[39:47, 414:560]
    # cv2.rectangle(my_range, (10, 0), (16, 4), (255, 0, 0), 1)
    # cv2.imwrite("data/image/my_band_default.png", my_band)

    # my_pinch
    cv2.rectangle(image, (180, 24), (230, 40), (255, 0, 0), 1)
    # pinch = image[24:40, 180:230]
    # cv2.rectangle(image, (235, 20), (348, 50), (255, 0, 0), 1)
    # cv2.rectangle(image, (414, 17), (560, 53), (255, 0, 0), 1)

    # your_pinch
    # cv2.rectangle(image, (538, 24), (588, 40), (255, 0, 0), 1)
    # cv2.rectangle(image, (207, 17), (350, 53), (255, 0, 0), 1)
    # cv2.rectangle(image, (418, 21), (533, 50), (255, 0, 0), 1)

    # image = cv2.resize(image, (1920, 1080))
    cv2.imshow("image", image)
    if cv2.waitKey(0) == 27:
        exit()
