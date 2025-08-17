import cv2
from cvzone.PoseModule import PoseDetector

# Initialize Pose detector
detector = PoseDetector()

# Start webcam
cap = cv2.VideoCapture(0)

counter = 0
stage = None  # "down" or "up"

while True:
    success, img = cap.read()
    if not success:
        break

    # Find pose
    img = detector.findPose(img)
    lmList, bbox = detector.findPosition(img, bboxWithHands=False)

    if lmList:
        # Get shoulder and elbow
        shoulder = lmList[11]  # Left shoulder
        elbow = lmList[13]     # Left elbow

        # Compare elbow Y with shoulder Y
        if elbow[2] > shoulder[2]:  # Going down
            stage = "down"
        if elbow[2] < shoulder[2] and stage == "down":  # Coming up
            stage = "up"
            counter += 1
            print(f"Push-up count: {counter}")

    # Show counter on screen
    cv2.putText(img, f'Push-ups: {counter}', (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow("AI Fitness Buddy - Push-up Counter", img)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

