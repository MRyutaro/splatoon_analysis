import cv2
import time

# 認識範囲
# 味方ブキアイコン位置
raw_xmin, raw_xmax = 525, 880
raw_ymin, raw_ymax = 40, 140
xmin, xmax = round(raw_xmin/2.5), round(raw_xmax/2.5)
ymin, ymax = round(raw_ymin/2.5), round(raw_ymax/2.5)

# 動画読み込みの設定
movie = cv2.VideoCapture('../data/a.mp4')
# movie = cv2.VideoCapture(0)

# 背景差分の設定
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

# ファイルからフレームを1枚ずつ取得して動画処理後に保存する
while True:
    ret, frame = movie.read()
    # フレーム取得 # フレームが取得できない場合はループを抜ける
    if not ret:
        break

    # フレームのサイズ変更
    # height = frame.shape[0]
    # width = frame.shape[1]
    # frame = cv2.resize(frame, (round(2.5*width), round(2.5*height)))

    detframe = frame[ymin:ymax, xmin:xmax]  # 背景差分する範囲を指定
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)  # 指定範囲に赤枠

    # ここからーーーーーーーーーーーーーーーーーー
    fgmask = fgbg.apply(detframe)  # 前景領域のマスクを取得
    moment = cv2.countNonZero(fgmask)  # 動体検知した画素数を取得
    text = 'Motion:' + str(moment)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, (20, 400), font, 1,
                (0, 255, 0), 2, cv2.LINE_AA)  # フレームに表示
    # ここまで変えるーーーーーーーーーーーーーーー

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    time.sleep(0.024)

# 撮影用オブジェクトとウィンドウの解放
movie.release()
