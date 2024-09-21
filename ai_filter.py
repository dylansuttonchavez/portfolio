import cv2

# Load classifiers
face_metod = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the hat image once
hat = cv2.imread('static/mexican_hat.png', -1)

def image_overlay(background, image, position=(0, 0)):
    if image.shape[2] != 4:
        return background  # Ensure the image has an alpha channel

    overlay_alpha = image[:, :, 3] / 255.0
    background_alpha = 1.0 - overlay_alpha
    x, y = position

    for c in range(3):
        background[y:y + image.shape[0], x:x + image.shape[1], c] = (
            overlay_alpha * image[:, :, c] +
            background_alpha * background[y:y + image.shape[0], x:x + image.shape[1], c]
        )

    return background

def generate_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Convert to grayscale
        image_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Face detection
        faces = face_metod.detectMultiScale(image_bw, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

        for (x, y, l, h) in faces:
            # Resize the hat only if necessary
            resized_hat = cv2.resize(hat, (l, h)) if hat.shape[1] != l or hat.shape[0] != h else hat
            frame = image_overlay(frame, resized_hat, (x, y - 150))

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')