import cv2


if __name__ == "__main__":
    # ゲーム開始
    # image_path = "./data/image/start.png"
    # ゲーム終了
    # image_path = "./data/image/finish3.png"
    # マップ開いてる
    # image_path = "./data/image/map.png"
    for i in range(9):
        # ピンチの判定
        image_path = f"./data/image/pinch/friend/{i}.png"
        # image_path = f"./data/image/pinch/enemy/{i}.png"
        image = cv2.imread(image_path)
        image = cv2.resize(image, (768, 432))

        bgr_frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray_frame, 130, 255, cv2.THRESH_BINARY)

        # cv2.imshow("image", image)
        # cv2.imshow("image", gray_frame)
        cv2.imshow("image", binary)
        if cv2.waitKey(0) == 27:
            exit()
