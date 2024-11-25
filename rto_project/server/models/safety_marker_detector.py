import torch
import torchvision.models as models


class SafetyMarkerDetector:
    def __init__(self):
        self.model = models.mobilenet_v3_small(pretrained=True)
        self.model.classifier[3] = torch.nn.Linear(
            self.model.classifier[3].in_features, 2)
        self.model.load_state_dict(
            torch.load('weights/safety_marker_detector.pth'))
        self.model.eval()

    def check_markers(self, image):
        transform = torchvision.transforms.Compose([
            torchvision.transforms.ToPILImage(),
            torchvision.transforms.Resize((224, 224)),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(
                [0.485, 0.456, 0.406],
                [0.229, 0.224, 0.225])
        ])

        image_tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            output = self.model(image_tensor)
            return bool(output.argmax().item())
