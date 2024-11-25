import easyocr
import torch

class LicensePlateDetector:
    def __init__(self):
        self.plate_detector = torch.hub.load(
            'ultralytics/yolov5',
            'custom',
            'weights/plate_detector.pt'
        )
        self.reader = easyocr.Reader(['en'])

    def detect_and_read(self, image):
        results = self.plate_detector(image)
        if len(results.pred[0]) > 0:
            bbox = results.pred[0][0].cpu().numpy()
            plate_roi = image[
                int(bbox[1]):int(bbox[3]),
                int(bbox[0]):int(bbox[2])
            ]
            ocr_result = self.reader.readtext(plate_roi)
            if ocr_result:
                return ocr_result[0][1]
        return None
