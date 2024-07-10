import os
import yaml
import shutil
import random

dir = 'datasets'
base_dir = f'{dir}/datasets'
images_dir = os.path.join(base_dir, 'images')
labels_dir = os.path.join(base_dir, 'labels')
train_images_dir = os.path.join(images_dir, 'train')
val_images_dir = os.path.join(images_dir, 'val')
train_labels_dir = os.path.join(labels_dir, 'train')
val_labels_dir = os.path.join(labels_dir, 'val')

os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

annotations_dir = './raw/annotations'
annotations_files = [f for f in os.listdir(annotations_dir) if f.endswith('.yml')]

classes = set()
print("Extracting class names...")
for annotation_file in annotations_files:
    with open(os.path.join(annotations_dir, annotation_file), 'r') as file:
        yaml_content = yaml.safe_load(file)
    try:
        objects = yaml_content['annotation']['object']
    except KeyError:
        objects = []
    for obj in objects:
        classes.add(obj['name'])

classes = sorted(list(classes))
print(f"{len(classes)} classes found")
print(classes)

# Function to convert annotations to YOLO format
def convert_annotation(yaml_content, img_width, img_height):
    try:
        objects = yaml_content['annotation']['object']
    except KeyError:
        objects = []
    yolo_annotations = []
    for obj in objects:
        class_name = obj['name']
        class_id = classes.index(class_name)
        bndbox = obj['bndbox']
        xmin, xmax = int(bndbox['xmin']), int(bndbox['xmax'])
        ymin, ymax = int(bndbox['ymin']), int(bndbox['ymax'])
        x_center = (xmin + xmax) / 2 / img_width
        y_center = (ymin + ymax) / 2 / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height
        yolo_annotations.append(f"{class_id} {x_center} {y_center} {width} {height}")
    return yolo_annotations

combined_files = list(zip(annotations_files, [os.path.join('./raw/images', f.replace('.yml', '.png')) for f in annotations_files]))
random.shuffle(combined_files)
split_index = int(len(combined_files) * 0.7)
train_files = combined_files[:split_index]
val_files = combined_files[split_index:]

def process_and_copy_files(file_list, dest_images_dir, dest_labels_dir):
    for annotation_file, image_file in file_list:
        with open(os.path.join(annotations_dir, annotation_file), 'r') as file:
            yaml_content = yaml.safe_load(file)

        filename = yaml_content['annotation']['filename']
        img_width = int(yaml_content['annotation']['size']['width'])
        img_height = int(yaml_content['annotation']['size']['height'])
        
        try:
            yolo_annotations = convert_annotation(yaml_content, img_width, img_height)
        except Exception as e:
            continue
        
        label_filename = filename.replace('.png', '.txt')
        with open(os.path.join(dest_labels_dir, label_filename), 'w') as label_file:
            label_file.write('\n'.join(yolo_annotations))
        
        shutil.copy(image_file, os.path.join(dest_images_dir, filename))

print("Processing training files...")
process_and_copy_files(train_files, train_images_dir, train_labels_dir)

print("Processing validation files...")
process_and_copy_files(val_files, val_images_dir, val_labels_dir)

yolo_yaml = {
    'train': "./images/train",
    'val': "./images/val",
    'nc': len(classes),
    'names': classes
}

with open(os.path.join(dir, 'dataset.yaml'), 'w') as yaml_file:
    yaml.dump(yolo_yaml, yaml_file, default_flow_style=False)

print("Dataset and YAML configuration file created successfully.")
