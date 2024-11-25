import torch
import torchvision.transforms as transforms


class TractorDetector:
    def __init__(self):
        # Load YOLOv5 model trained for tractor detection
        self.model = torch.hub.load(
            'ultralytics/yolov5',
            'custom',
            'weights/tractor_detector.pt'
        )
        self.model.conf = 0.5  # Confidence threshold

    def detect(self, image):
        """
        Detect tractors in image
        Args:
            image: Input image
        Returns:
            bool: True if tractor detected, False otherwise
        """
        results = self.model(image)

        # Check if any detections with tractor class
        if len(results.pred[0]) > 0:
            for det in results.pred[0]:
                if int(det[-1]) == 0:  # Assuming tractor is class 0
                    return True
        return False