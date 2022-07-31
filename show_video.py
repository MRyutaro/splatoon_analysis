import cv2

movie = cv2.VideoCapture(1)
width = movie.get(cv2.CAP_PROP_FRAME_WIDTH)
height = movie.get(cv2.CAP_PROP_FRAME_HEIGHT)
# movie.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# movie.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    ret, frame = movie.read()
    # フレーム取得 # フレームが取得できない場合はループを抜ける
    if not ret:
        break
    # キー操作があればwhileループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('frame', cv2.resize(frame, (int(768), int(432))))
    cv2.waitKey(1)

# 撮影用オブジェクトとウィンドウの解放
movie.release()
