import cv2
import os

# Set path to your actual Windows Pictures folder
pictures_dir = r"C:\Users\miahm\OneDrive\Pictures"

# Make sure the folder exists
os.makedirs(pictures_dir, exist_ok=True)

# Open webcam
cap = cv2.VideoCapture(0)

snapshot_count = 1  # Counter for unique filenames

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Webcam Feed", frame)

    # Capture key press
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):  # Quit
        print("Exiting...")
        break
    elif key == ord('s'):  # Save snapshot
        filename = os.path.join(pictures_dir, f"snapshot{snapshot_count}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")
        snapshot_count += 1

# Release resources properly
cap.release()
cv2.destroyAllWindows()

















