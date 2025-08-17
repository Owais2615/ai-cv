import cv2
import datetime
import os

# =============================
# Set your save locations here:
# =============================
PICTURES_FOLDER = r"C:\Users\miahm\OneDrive\Pictures"
VIDEOS_FOLDER   = r"C:\Users\miahm\Videos\Captures"
# (⬆️ change these paths to wherever you want)

# Create folders if they don't exist
os.makedirs(PICTURES_FOLDER, exist_ok=True)
os.makedirs(VIDEOS_FOLDER, exist_ok=True)

# Start video capture
cap = cv2.VideoCapture(0)

# Background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=50, detectShadows=True)

# Video writer
out = None
recording = False
snapshot_count = 0

# Get frame size
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply background subtraction
    fgmask = fgbg.apply(frame)

    # Remove shadows (value 127 in mask)
    _, thresh = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 500:  # ignore very small movements
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Show "REC" text if recording
    if recording:
        cv2.putText(frame, "REC", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)

    # If recording, save frame
    if recording and out is not None:
        out.write(frame)

    # Show live video
    cv2.imshow("Motion Detection", frame)

    # Key handling
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):  # Quit
        break
    elif key == ord('r') and not recording:  # Start recording
        filename = datetime.datetime.now().strftime("recording_%Y%m%d_%H%M%S.mp4")
        filepath = os.path.join(VIDEOS_FOLDER, filename)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # use mp4 codec
        out = cv2.VideoWriter(filepath, fourcc, 20, (frame_width, frame_height))
        recording = True
        print(f"Started recording: {filepath}")
    elif key == ord('t') and recording:  # Stop recording
        recording = False
        out.release()
        out = None
        print("Stopped recording.")
    elif key == ord('s'):  # Save snapshot
        snapshot_count += 1
        snap_filename = os.path.join(PICTURES_FOLDER, f"snapshot_{snapshot_count}.png")
        cv2.imwrite(snap_filename, frame)
        print(f"Snapshot saved: {snap_filename}")

# Cleanup
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
























