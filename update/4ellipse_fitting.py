import cv2
import time

# 認識範囲
# 味方ブキアイコン位置
raw_xmin, raw_xmax = 515, 880
raw_ymin, raw_ymax = 30, 150
xmin, xmax = round(raw_xmin/2.5), round(raw_xmax/2.5)
ymin, ymax = round(raw_ymin/2.5), round(raw_ymax/2.5)
# xmin, xmax = 350, 450
# ymin, ymax = 220, 330

# 動画読み込みの設定
movie = cv2.VideoCapture('./data/a.mp4')
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

    # BGR -> grayscale
    gray = cv2.cvtColor(cv2.bitwise_not(detframe), cv2.COLOR_BGR2GRAY)

    # 閾値処理
    _, binary = cv2.threshold(gray, 95, 255, cv2.THRESH_BINARY)

    #  輪郭抽出
    contours, _ = cv2.findContours(
        binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 小さい輪郭は誤検出として削除
    contours = list(filter(lambda x: cv2.contourArea(x) > 100, contours))

    # 輪郭を囲む長方形に変換
    # rects = [cv2.boundingRect(cnt) for cnt in contours]
    for _, cnt in enumerate(contours):
        # 楕円フィッティング
        if len(cnt) > 5:
            center, (width, height), angle = cv2.fitEllipse(cnt)

            # 楕円描画
            cv2.ellipse(
                frame, ((center[0]+xmin, center[1]+ymin),
                        (width, height), angle),
                (255, 0, 0), 2)

    # cv2.drawContours(frame, contours, -1, (0, 0, 255), 1, cv2.LINE_AA)
    # 長方形を描画する。
    bgr = frame.copy()
    # for x, y, width, height in rects:

    #     cv2.rectangle(bgr, (x, y), (x + width, y + height), (255, 0, 0), 2)
    # 指定範囲に赤枠
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    time.sleep(0.024)

# 撮影用オブジェクトとウィンドウの解放
movie.release()
