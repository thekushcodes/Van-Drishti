import cv2
from ultralytics import YOLO

# Load your trained model
model = YOLO("models/best.pt")

# Input video
input_video = "forest.mp4"

# Open video
video = cv2.VideoCapture(input_video)

if not video.isOpened():
    print("Could not open video.")
    exit()

# Get video properties
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

# Create output video
output_video = "wildlife_detection.mp4"

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

writer = cv2.VideoWriter(
    output_video,
    fourcc,
    fps,
    (width, height)
)

print("Processing video...")

while True:

    success, frame = video.read()

    if not success:
        break

    # Run YOLO on this frame
    results = model(frame, conf=0.5)

    # Draw detections
    annotated_frame = results[0].plot()

    # Save frame to output video
    writer.write(annotated_frame)

    # Show live processing
    cv2.imshow("Wildlife Detection", annotated_frame)

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
writer.release()
cv2.destroyAllWindows()

print(f"\nDone.")
print(f"Output saved as: {output_video}")