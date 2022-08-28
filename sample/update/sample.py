import cv2
import time

# Video Reader を作成
cap = cv2.VideoCapture('data/a.mp4')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

xmin, xmax = 200, 600
ymin, ymax = 100, 400

prev_frame = None
while True:
    ret, frame = cap.read()
    if not ret:
        break

    if prev_frame is not None:
        # BGR -> grayscale
        prev_gray = cv2.cvtColor(
            prev_frame[ymin:ymax, xmin:xmax], cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(frame[ymin:ymax, xmin:xmax], cv2.COLOR_BGR2GRAY)
        # 差分を計算
        diff = cv2.absdiff(gray, prev_gray)
        # 閾値処理
        _, binary = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
        #  輪郭抽出
        _, contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,
                                          offset=(xmin, ymin))
        # 面積でフィルタリング
        contours = list(
            filter(lambda cnt: cv2.contourArea(cnt) > 1000, contours))
        # 輪郭を囲む長方形に変換
        rects = [cv2.boundingRect(cnt) for cnt in contours]
        # 長方形を描画する。
        bgr = frame.copy()
        for x, y, width, height in rects:
            cv2.rectangle(bgr, (x, y), (x + width, y + height), (0, 255, 0), 2)
        cv2.rectangle(bgr, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)

        cv2.imshow('frame', frame)
    cv2.waitKey(1)
    time.sleep(0.024)

    prev_frame = frame

cap.release()
cv2.destroyAllWindows()
