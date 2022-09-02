import cv2
import time
import numpy as np

# -------------------------------------
# class TrainImage():
# video
# -> (学習させたい動画のパス、学習させたい範囲、学習させたいラベルの名前)
# -> {"range": "range_list",
#    "color": "color_list"}

# binarize(bgr_image) -> binary
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# _, binary = cv2.threshold(gray_image, 95, 255, cv2.THRESH_BINARY)

# split(image_in_search_range, width_split_num, height_split_num) -> split_images
# image_in_search_range=[[x_min, y_min], [x_max, y_max]]
# search_range_width, search_range_height=
# 縦横を数でわって、それをlistに入れていく
# 余ったやつは捨てる
# for文で
# image[ymin:ymax, xmin:xmax]
# にしてsplit_imagesにappend
# split_images=[[image0, image1, ...], [image0, image1, ...], ...]
# (len(split_images)=height_split_num
# len(split[0])=width_split_num)
# (pinchの場合、
# friend_pinch_spilit = cut(binary[24:40, 180:230], )
# enemy_pinch_spilit = cut(binary[24:40, 538:588], )
# )
# ずっと白or黒が入ってる範囲を引数に
# いちいち範囲を調べるのだるい、、


# find_means_of(split_images) -> color_mean_list_in_range
# split_images=[[image0, image1, ...], [image0, image1, ...], ...]
# color_mean_list_in_range=[[10, 13, ...]. [9, 11, ...], ...]
# (len(color_mean_list_in_range)=height_split_num,
#  len(color_mean_list_in_range[i])=width_split_num)

# ここからはwhile文を抜けてから。
# create_learned_color_list(color_mean_list_in_range) -> learned_color_list
# すべてのフレームの中での最頻値を学習済みデータとする

# output2json(label, learned_color_list) -> jsonファイル出力
# {"label": learned_color_list}
# の形でjsonファイルに書き込む

# ------------------------------------------
# class TestImage(game_transition: str):
# video -> flag

# read_learned_color() -> learned_color=list:
# json

# clip_image(learned_range: list) -> clipped_image=list:

# matche_the_image(learned_color: list, clipped_image: list) -> flag=boolean:
# 誤差込みで認識する
# np.allclose(learned_color_list, clipped_image, rtol=??, atol=??)を使う
# aとbを比較する
# この場合aとbはlistの要素の一つ？↓の関数で使われる変数が何なのか調べる
# np.allcloseの戻り値は何なのか
# if 誤差 = absolute(a-b) <= (atol + rtol*absolute(b)) なら一致すると判定

# recognize(image, label: str, learned_range: list, learned_color: list) -> label=str:

# main():
#   while movie.isOpened:
#       ret, frame = movie.read()
#       recognize()


# ----------------------------------------------

if __name__ == "__main__":
    movie = cv2.VideoCapture('./data/video/area.mp4')
    # movie = cv2.VideoCapture('./data/video/pinch/area_mypinch_only.mp4')
    # movie = cv2.VideoCapture('./data/video/pinch/area_yourpinch_only.mp4')

    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))

        # 0 = default, 1 = friend, 2 = enemy
        cv2.rectangle(frame, (180, 24), (230, 40), (255, 0, 0), 1)
        cv2.rectangle(frame, (538, 24), (588, 40), (255, 0, 0), 1)

        if cv2.waitKey(1) == 27:
            break

        cv2.imshow('frame', frame)
        time.sleep(0.02)

    movie.release()
