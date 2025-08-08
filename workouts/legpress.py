import cv2
import ultralytics
from ultralytics import solutions
import mediapipe as mp

# Set output frame size for display
output_size = (800, 600)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Open video file
cap = cv2.VideoCapture("Legpress.demo.video.mp4")
assert cap.isOpened(), "Error reading video file"

# Initialize AIGym
gym = solutions.AIGym(
    show=False,  # Display the frame
    kpts=[11, 13, 15],  # keypoints index for leg press
    model="yolo11m-pose.pt",  # Path to the YOLO11 pose estimation model file
    line_width=4,  # Adjust the line width for bounding boxes and text display
    up_angle=140,
    down_angle=120,
    verbose=False,
)

show_2d = False  # Flag for 2D mapping

# Frame processing loop
while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing completed.")
        break

    # Run YOLO pose estimation
    results = gym(im0)
    frame = results.plot_im

    if show_2d:
        # Add MediaPipe pose estimation
        rgb_frame = cv2.cvtColor(im0, cv2.COLOR_BGR2RGB)  # Use original frame for MediaPipe
        mp_results = pose.process(rgb_frame)
        
        if mp_results.pose_landmarks:
            # Draw MediaPipe skeleton in bright colors
            mp_drawing.draw_landmarks(
                frame,  # Draw on the YOLO output
                mp_results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(
                    color=(0, 255, 255),  # Yellow dots
                    thickness=4,
                    circle_radius=4
                ),
                connection_drawing_spec=mp_drawing.DrawingSpec(
                    color=(255, 255, 0),  # Cyan lines
                    thickness=4,
                )
            )
            print("MediaPipe landmarks drawn")

    # Resize frame for display
    resized_frame = cv2.resize(frame, output_size)

    # Show output
    cv2.imshow("Exercise Pose Estimation", resized_frame)

    # Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('m'):
        show_2d = not show_2d  # Toggle 2D mapping
        print(f"2D Mapping {'Enabled' if show_2d else 'Disabled'} - Key press detected")

# Cleanup
cap.release()
cv2.destroyAllWindows()
pose.close()
