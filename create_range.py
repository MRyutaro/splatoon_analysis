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
    # image_path = "./data/image/default.png"
    # image_path = "./data/image/pinch/friend/0.png"
    image_path = "./data/image/pinch/enemy/0.png"
    # ゲーム開始
    # image_path = "./data/image/start.png"
    # ゲーム終了
    # image_path = "./data/image/finish.png"
    # マップ開いてる
    # image_path = "./data/image/map.png"
    image = cv2.imread(image_path)
    image = cv2.resize(image, (768, 432))

    # ピンチの判定--------------------------------------------------------
    # 味方のピンチの範囲
    cv2.rectangle(image, (184, 20), (214, 29), (255, 0, 0), 1)
    # 敵のピンチの範囲
    cv2.rectangle(image, (554, 20), (584, 29), (255, 0, 0), 1)

    # イカメーター in デフォルト
    cv2.rectangle(image, (213, 11), (351, 43), (255, 0, 0), 1)
    # cv2.rectangle(image, (417, 11), (555, 43), (255, 0, 0), 1)

    # # イカメーター in 味方がピンチ
    cv2.rectangle(image, (227, 13), (348, 42), (255, 0, 0), 1)
    # cv2.rectangle(image, (414, 10), (569, 45), (255, 0, 0), 1)

    # # イカメーター in 敵がピンチ
    cv2.rectangle(image, (197, 10), (352, 45), (255, 0, 0), 1)
    # cv2.rectangle(image, (418, 13), (539, 42), (255, 0, 0), 1)

    # ゲームの開始の判定--------------------------------------------------
    # cv2.rectangle(image, (365, 21), (375, 38), (255, 0, 0), 1)

    # ゲームの終了の判定--------------------------------------------------
    # cv2.rectangle(image, (160, 260), (300, 270), (255, 0, 0), 1)
    # cv2.rectangle(image, (540, 195), (680, 205), (255, 0, 0), 1)

    # マップを開いているかの判定------------------------------------------
    # cv2.rectangle(image, (31, 204), (37, 226), (255, 0, 0), 1)
    # cv2.rectangle(image, (595, 204), (601, 226), (255, 0, 0), 1)
    # cv2.rectangle(image, (305, 32), (327, 38), (255, 0, 0), 1)

    # image = cv2.resize(image, (1920, 1080))
    cv2.imshow("image", image)
    if cv2.waitKey(0) == 27:
        exit()
