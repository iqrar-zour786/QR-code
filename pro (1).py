import cv2
from pyzbar.pyzbar import decode
import webbrowser

def decode_qr_and_open_url(image):
    # Decode QR codes in the image
    qr_codes = decode(image)
    
    for qr in qr_codes:
        qr_data = qr.data.decode('utf-8')  # Decode the QR code data
        qr_type = qr.type  # Get QR code type

        # Draw a bounding box around the QR code
        points = qr.polygon
        if len(points) == 4:
            import numpy as np
        pts = np.array(points, dtype=int).reshape((-1, 1, 2))

        
        # Show the decoded QR code data
        cv2.putText(image, qr_data, (qr.rect[0], qr.rect[1] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        print(f"Detected QR Code: {qr_data}")
        
        # Open the decoded link in the default web browser
        if qr_data.startswith("http://") or qr_data.startswith("https://"):
            print(f"Opening URL: {qr_data}")
            webbrowser.open(qr_data)

    return image

# Initialize webcam
cap = cv2.VideoCapture(0)

print("Starting QR Scanner. Point it at a QR code to scan...")
print("Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error accessing webcam. Exiting...")
        break

    # Process the frame to detect and decode QR codes
    frame = decode_qr_and_open_url(frame)

    # Display the frame with bounding boxes
    cv2.imshow('QR Code Scanner', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

