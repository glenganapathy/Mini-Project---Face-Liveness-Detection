import os
import cv2
import numpy as np
import warnings
import time
import argparse
from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name

warnings.filterwarnings('ignore')

def resize_to_aspect_ratio(image, target_width, target_height):
    """Resize image to the target aspect ratio."""
    return cv2.resize(image, (target_width, target_height))

def test(frame, model_dir, device_id):
    """Run anti-spoofing tests on the given frame."""
    model_test = AntiSpoofPredict(device_id)
    image_cropper = CropImage()

    # Get original frame dimensions
    orig_height, orig_width = frame.shape[:2]

    # Resize frame to 3:4 aspect ratio for processing
    new_width = int(orig_height * 3 / 4)
    resized_frame = resize_to_aspect_ratio(frame, new_width, orig_height)

    # Detect face bounding box on resized frame
    image_bbox = model_test.get_bbox(resized_frame)

    # Scale bounding box coordinates back to original dimensions
    scale_x = orig_width / new_width
    scale_y = orig_height / orig_height  # No height change
    scaled_bbox = [
        int(image_bbox[0] * scale_x),
        int(image_bbox[1] * scale_y),
        int(image_bbox[2] * scale_x),
        int(image_bbox[3] * scale_y),
    ]

    prediction = np.zeros((1, 3))
    test_speed = 0

    # Run anti-spoofing predictions using models
    for model_name in os.listdir(model_dir):
        h_input, w_input, model_type, scale = parse_model_name(model_name)
        param = {
            "org_img": resized_frame,
            "bbox": image_bbox,
            "scale": scale,
            "out_w": w_input,
            "out_h": h_input,
            "crop": True,
        }
        if scale is None:
            param["crop"] = False
        img = image_cropper.crop(**param)
        start = time.time()
        prediction += model_test.predict(img, os.path.join(model_dir, model_name))
        test_speed += time.time() - start

    # Process predictions
    label = np.argmax(prediction)
    value = prediction[0][label] / 2
    if label == 1:
        result_text = "Real Face Score: {:.2f}".format(value)
        color = (0, 255, 0)  # Green for real face
    else:
        result_text = "Fake Face Score: {:.2f}".format(value)
        color = (0, 0, 255)  # Red for fake face

    # Draw bounding box and result text on the original frame
    cv2.rectangle(
        frame,
        (scaled_bbox[0], scaled_bbox[1]),
        (scaled_bbox[0] + scaled_bbox[2], scaled_bbox[1] + scaled_bbox[3]),
        color,
        2,
    )
    cv2.putText(
        frame,
        result_text,
        (scaled_bbox[0], scaled_bbox[1] - 5),
        cv2.FONT_HERSHEY_COMPLEX,
        1.0,
        color,
        thickness=2,
    )

    return frame

def video_feed(model_dir, device_id):
    """Capture video feed and run anti-spoofing detection."""
    cap = cv2.VideoCapture(0)  # Use default webcam
    if not cap.isOpened():
        print("Error: Cannot access the webcam.")
        return

    cv2.namedWindow("Anti-Spoofing Detection", cv2.WND_PROP_FULLSCREEN)

    print("Press 'ESC' to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        # Get the original dimensions of the captured frame
        orig_height, orig_width = frame.shape[:2]

        # Resize the frame while maintaining the aspect ratio
        aspect_ratio = orig_height / orig_width
        window_width = 800  # Set a default width or get from your screen size
        window_height = 600  # Set a default height or get from your screen size

        if aspect_ratio > 1:  # Portrait
            new_height = window_height
            new_width = int(window_height / aspect_ratio)
        else:  # Landscape
            new_width = window_width
            new_height = int(window_width * aspect_ratio)

        # Resize the frame
        frame_resized = cv2.resize(frame, (new_width, new_height))

        # Run test function for anti-spoofing detection
        try:
            processed_frame = test(frame_resized, model_dir, device_id)
        except Exception as e:
            print("Error during detection:", e)
            processed_frame = frame_resized

        # Display the frame with detections
        cv2.imshow("Anti-Spoofing Detection", processed_frame)

        # Exit loop on 'ESC' key
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    desc = "Video feed anti-spoofing test"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--device_id",
        type=int,
        default=0,
        help="which gpu id, [0/1/2/3]"
    )
    parser.add_argument(
        "--model_dir",
        type=str,
        default="./resources/anti_spoof_models",
        help="model_lib used to test"
    )
    args = parser.parse_args()
    video_feed(args.model_dir, args.device_id)