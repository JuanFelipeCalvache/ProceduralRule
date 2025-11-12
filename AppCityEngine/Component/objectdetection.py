from ultralytics import YOLO
import cv2
import sys

class ObjectDetectionModel:
    def __init__(self, model_path):
        # Cargar el modelo YOLOv8
        self.model = YOLO(model_path)

    def detect_image(self, image_path):
        results = self.model(image_path)  # Realizar la detección directamente
        detections = []

        for result in results:
            boxes = result.boxes
            names = result.names
            for box in boxes:
                detection = {
                    'xmin': box.xyxy[0][0].item(),
                    'ymin': box.xyxy[0][1].item(),
                    'xmax': box.xyxy[0][2].item(),
                    'ymax': box.xyxy[0][3].item(),
                    'confidence': box.conf[0].item(),
                    'class': int(box.cls[0].item()),
                    'name': names[int(box.cls[0].item())]
                }
                detections.append(detection)

        return detections

    @staticmethod
    def classify_floors_by_windows_and_balconies(detections, vertical_threshold=30):
        filtered_detections = [d for d in detections if d['name'] in ['window', 'balcony']]
        filtered_detections.sort(key=lambda x: x['ymin'])

        floors = []
        current_floor = []

        for i, det in enumerate(filtered_detections):
            if i == 0:
                current_floor.append(det)
            else:
                if det['ymin'] - filtered_detections[i-1]['ymin'] > vertical_threshold:
                    floors.append(current_floor)
                    current_floor = [det]
                else:
                    current_floor.append(det)

        if current_floor:
            floors.append(current_floor)

        floors.reverse()

        has_windows_or_balconies = len(filtered_detections) > 0
        ventanas_por_piso = [(sum(1 for d in floor if d['name'] == 'window'),
                              sum(1 for d in floor if d['name'] == 'balcony')) for floor in floors]

        total_windows = sum(ventanas[0] for ventanas in ventanas_por_piso)
        total_balconies = sum(ventanas[1] for ventanas in ventanas_por_piso)

        if total_windows > 0 and total_balconies > 0:
            predominant_type = 'both'
        elif total_windows > 0:
            predominant_type = 'window'
        elif total_balconies > 0:
            predominant_type = 'balcony'
        else:
            predominant_type = None

        cantidad_por_piso = []
        for ventanas, balcones in ventanas_por_piso:
            cantidad_por_piso.append(ventanas + balcones)

        return floors, has_windows_or_balconies, predominant_type, cantidad_por_piso

    @staticmethod
    def draw_boxes_and_count(image_path, detections, floors):
        img = cv2.imread(image_path)

        for det in detections:
            xmin, ymin, xmax, ymax = int(det['xmin']), int(det['ymin']), int(det['xmax']), int(det['ymax'])
            label = f"{det['name']} {det['confidence']:.2f}"
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(img, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        for i, floor in enumerate(floors):
            window_count = sum(1 for det in floor if det['name'] == 'window')
            balcony_count = sum(1 for det in floor if det['name'] == 'balcony')
            print(f"Piso {i+1}: {window_count} Windows, {balcony_count} Balconies")
            cv2.putText(img, f"Floor {i+1}: {window_count} Windows, {balcony_count} Balconies", 
                        (10, 30 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        cv2.imwrite(image_path.replace('.jpg', '_annotated.jpg'), img)

# Ejemplo de uso
if __name__ == "__main__":
    model_path = "yolov8n.pt"  # Tu modelo YOLOv8
    image_path = "AppCityEngine/yolov5/imagenes/build9.jpg"

    model = ObjectDetectionModel(model_path)
    detections = model.detect_image(image_path)
    floors, has_windows_or_balconies, predominant_type, cantidad_por_piso = model.classify_floors_by_windows_and_balconies(detections)
    model.draw_boxes_and_count(image_path, detections, floors)
