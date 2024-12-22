from flask import Flask, jsonify, request
import cv2

app = Flask(__name__)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

@app.route('/detect-face', methods=['GET'])
def detect_face():

    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    if not ret:
        return jsonify({"error": "Unable to capture frame from webcam."}), 500

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRA)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    cap.release()
    cv2.imshow('Debug Frame', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(faces) > 0:
        return jsonify({"face_detected": True})
    else:
        return jsonify({"face_detected": False})

if __name__ == "__main__":
    app.run(debug=True)


