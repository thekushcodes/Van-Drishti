import cv2
from ultralytics import YOLO

model = YOLO("models/best.pt")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open webcam.")
    exit()

while True:
    success, frame = camera.read()

    if not success:
        print("Could not read frame.")
        break

    results = model(frame, conf=0.5)

    annotated_frame = results[0].plot()

    cv2.imshow("Wildlife Detection - YOLO26n", annotated_frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()