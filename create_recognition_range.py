# video
# ->
# game_transition, label, {"target": "range_lsit"}

# まずはrecrangleで場所を指定する。
# そのあと切り取りをしてチェックをする。
# 色がでた数を表示できるようにする。
# unique, counts = np.unique(clipped_range, return_counts=True)
# result = np.column_stack((unique, counts))
# ↑これ
# game_trantision, label, {"target": "range_lsit"}
# label判定するのに何か所か判定場所が必要。
# それがtarget

import cv2


if __name__ == "__main__":
    # ピンチの判定
    image_path = "./data/image/friend_pinch.png"
    # image_path = "./data/image/enemy_pinch.png"
    # ゲーム開始
    # image_path = "./data/image/start.png"
    # ゲーム終了
    # image_path = "./data/image/finish.png"
    # マップ開いてる
    # image_path = "./data/image/map.png"
    image = cv2.imread(image_path)
    image = cv2.resize(image, (768, 432))

    # ピンチの判定--------------------------------------------------------
    # friend pinch
    cv2.rectangle(image, (175, 16), (220, 33), (255, 0, 0), 1)
    # enemy pinch
    cv2.rectangle(image, (545, 16), (590, 33), (255, 0, 0), 1)

    # # ika icons in friend pinch
    # cv2.rectangle(image, (227, 13), (348, 42), (255, 0, 0), 1)
    # cv2.rectangle(image, (414, 10), (569, 45), (255, 0, 0), 1)

    # # ika icons in enemy pinch
    # cv2.rectangle(image, (197, 10), (352, 45), (255, 0, 0), 1)
    # cv2.rectangle(image, (418, 13), (539, 42), (255, 0, 0), 1)

    # ゲームの開始の判定--------------------------------------------------
    # cv2.rectangle(image, (365, 21), (375, 38), (255, 0, 0), 1)

    # ゲームの終了の判定--------------------------------------------------
    # cv2.rectangle(image, (161, 255), (307, 278), (255, 0, 0), 1)
    # cv2.rectangle(image, (537, 188), (673, 211), (255, 0, 0), 1)

    # マップを開いているかの判定------------------------------------------
    # cv2.rectangle(image, (31, 204), (37, 226), (255, 0, 0), 1)
    # cv2.rectangle(image, (595, 204), (601, 226), (255, 0, 0), 1)
    # cv2.rectangle(image, (305, 32), (327, 38), (255, 0, 0), 1)

    # image = cv2.resize(image, (1920, 1080))
    cv2.imshow("image", image)
    if cv2.waitKey(0) == 27:
        exit()
