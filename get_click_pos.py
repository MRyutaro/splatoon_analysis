import cv2


def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


if __name__ == "__main__":
    # ピンチの判定
    image_path = "./data/image/default.png"
    # image_path = "./data/image/friend_pinch.png"
    # image_path = "./data/image/enemy_pinch.png"
    # ゲーム開始
    # image_path = "./data/image/start.png"
    # ゲーム終了
    # image_path = "./data/image/finish.png"
    # マップ開いてる
    # image_path = "./data/image/map.png"

    image = cv2.imread(image_path)
    cv2.imshow('image', cv2.resize(image, (768, 432)))
    cv2.setMouseCallback('image', onMouse)
    cv2.waitKey(0)
