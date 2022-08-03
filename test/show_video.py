import cv2

movie = cv2.VideoCapture(1)

while True:
    ret, frame = movie.read()
    if not ret:
        break

    frame = cv2.resize(frame, (768, 432))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('frame', frame)
    cv2.waitKey(1)

movie.release()
