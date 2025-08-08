import cv2
import ultralytics
from ultralytics import solutions

# Set output frame size for display
output_size = (800, 600)

# Open video file
cap = cv2.VideoCapture("Pushups.demo.video.mp4")
assert cap.isOpened(), "Error reading video file"

# Initialize AIGym
gym = solutions.AIGym(
    show=False,  # We'll handle showing manually
    kpts=[5, 7, 9],  # Keypoints for pushups: shoulder, elbow, wrist
    model="yolo11n-pose.pt",
    line_width=4,
    verbose=False
)

# Frame processing loop
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing completed.")
        break

    # Run pose estimation and analysis
    results = gym(im0)

    # Resize frame for display
    resized_frame = cv2.resize(results.plot_im, output_size)

    # Show output
    cv2.imshow("Pushups Pose Estimation", resized_frame)

    # Stop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
