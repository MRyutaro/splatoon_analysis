import cv2
import time

x_min, x_max = 200, 356
y_min, y_max = 16, 52

movie = cv2.VideoCapture('./data/video/asari.mp4')
# movie = cv2.VideoCapture(0)

if __name__ == "__main__":
    # 背景差分の設定
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    while True:
        ret, frame = movie.read()
        if not ret:
            break

        frame = cv2.resize(frame, (768, 432))

        # ここからーーーーーーーーーーーーーーーーーー
        fgmask = fgbg.apply(frame)  # 前景領域のマスクを取得
        moment = cv2.countNonZero(fgmask)  # 動体検知した画素数を取得
        text = 'Motion:' + str(moment)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, (20, 400), font, 1,
                    (0, 255, 0), 1, cv2.LINE_AA)  # フレームに表示
        # ここまで変えるーーーーーーーーーーーーーーー

        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        time.sleep(0.024)

    # 撮影用オブジェクトとウィンドウの解放
    movie.release()
