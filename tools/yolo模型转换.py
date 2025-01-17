# -*- coding: UTF-8 -*-
'''
@Project :AIProject 
@Author  :风吹落叶
@Contack :Waitkey1@outlook.com
@Version :V1.0
@Date    :2025/1/15 9:05 
@Describe:
'''
from ultralytics import YOLO

# Load the YOLO11 model
model = YOLO("L:\AIProject\AI标注器\models\yolo11x.pt")

# Export the model to ONNX format
model.export(format="onnx")  # creates 'yolo11n.onnx'

# Load the exported ONNX model
onnx_model = YOLO("yolo11n.onnx")

# Run inference
results = onnx_model("https://ultralytics.com/images/bus.jpg")