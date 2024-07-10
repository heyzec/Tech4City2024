from ultralytics import YOLO

dataset_yaml = './datasets/dataset.yaml'

model = YOLO('yolov8n.pt') 
# modify device to others if you are not using arm mac lol
model.train(data=dataset_yaml, epochs=1)

model.save('yolov8_custom.pt')