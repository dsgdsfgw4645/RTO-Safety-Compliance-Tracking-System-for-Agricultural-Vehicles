from flask import Flask, request, jsonify
from models.license_plate_detector import LicensePlateDetector
from models.safety_marker_detector import SafetyMarkerDetector
from models.tractor_detector import TractorDetector
from database import Database
import cv2
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
tractor_detector = TractorDetector()
license_detector = LicensePlateDetector()
safety_detector = SafetyMarkerDetector()
db = Database()

@app.route('/process_frame', methods=['POST'])
def process_frame():
    if 'frame' not in request.files:
        return jsonify({'error': 'No frame provided'}), 400

    # Read image
    file = request.files['frame']
    npimg = np.fromstring(file.read(), np.uint8)
    image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # First detect if tractor is present
    is_tractor = tractor_detector.detect(image)
    if not is_tractor:
        return jsonify({
            'is_tractor': False,
            'plate_number': None,
            'has_safety_markers': None
        })

    # Process tractor image
    plate_number = license_detector.detect_and_read(image)
    has_markers = safety_detector.check_markers(image)

    # Log violation if needed
    if plate_number and not has_markers:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        image_path = f'violations/{plate_number}_{timestamp}.jpg'
        cv2.imwrite(image_path, image)
        db.log_violation(plate_number, image_path)

    return jsonify({
        'is_tractor': True,
        'plate_number': plate_number,
        'has_safety_markers': has_markers
    })

if __name__ == '__main__':
    os.makedirs('violations', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
