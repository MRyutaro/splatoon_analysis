import cv2
import time

# cap = cv2.VideoCapture(1)

filepath = './data/video/asari.mp4'
cap = cv2.VideoCapture(filepath)


before = None

while True:
    ret, frame = cap.read()
    if ret is False:
        break

    # 白黒画像に変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if before is None:
        before = gray.astype("float")
        continue

    # 現在のフレームと移動平均との差を計算
    cv2.accumulateWeighted(gray, before, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(before))

    # frameDeltaの画像を２値化
    _, thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)

    # 輪郭のデータを取得
    contours, _ = cv2.findContours(thresh,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    # 差分があった点を画面に描画
    for target in contours:
        x, y, w, h = cv2.boundingRect(target)

        # 小さい変更点は無視
        # if w < 30:
        #     continue

        areaframe = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('frame', cv2.resize(frameDelta, (960, 540)))
    if cv2.waitKey(1) == 27:
        exit()
    time.sleep(0.02)

cv2.destroyAllWindows()
