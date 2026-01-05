from ultralytics import YOLO
import cv2
import time
import os
from twilio.rest import Client

# ===================== CONFIGURATION =====================
CONFIDENCE_THRESHOLD = 0.6
FRAME_SKIP = 3                 # Run detection every 3 frames
ALERT_COOLDOWN = 120           # Seconds

# ===================== TWILIO SETUP =====================
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")
client = Client(account_sid, auth_token)

# ===================== MODEL LOADING =====================
model = YOLO("yolov8n.pt")
model.to("cuda")  # Enable GPU acceleration on Jetson Nano

# ===================== MAIN FUNCTION =====================
def detect_elephant_live(camera_index=0):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)

    if not cap.isOpened():
        print("Camera access failed")
        return

    last_alert_time = 0
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 640))
        frame_count += 1
        elephant_detected = False

        # Run detection only every N frames
        if frame_count % FRAME_SKIP == 0:
            results = model(frame, verbose=False)

            for result in results:
                for box in result.boxes:
                    class_id = int(box.cls.item())
                    label = model.names[class_id]

                    if label.lower() == "elephant":
                        confidence = float(box.conf.item())

                        if confidence >= CONFIDENCE_THRESHOLD:
                            elephant_detected = True
                            x1, y1, x2, y2 = map(int, box.xyxy[0])

                            cv2.rectangle(frame, (x1, y1), (x2, y2),
                                          (0, 255, 0), 2)
                            cv2.putText(frame,
                                        f"Elephant {confidence:.2f}",
                                        (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.6, (0, 255, 0), 2)

        # ===================== ALERT LOGIC =====================
        current_time = time.time()
        if elephant_detected and (current_time - last_alert_time) > ALERT_COOLDOWN:
            client.messages.create(
                from_="+18782870242",
                to="+91XXXXXXXXXX",
                body="🚨 Elephant detected nearby. Please stay alert."
            )
            last_alert_time = current_time
            print("Alert sent successfully")

        cv2.imshow("Elephant Detection System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


detect_elephant_live(0)
