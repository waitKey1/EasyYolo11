# -*- coding: UTF-8 -*-
'''
@Project :AI标注器 
@Author  :风吹落叶
@Contack :Waitkey1@outlook.com
@Version :V1.0
@Date    :2025/1/15 11:04 
@Describe:
'''

import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO

if __name__ == '__main__':
    # model.load('yolo11n.pt') # 加载预训练权重,改进或者做对比实验时候不建议打开，因为用预训练模型整体精度没有很明显的提升
    model = YOLO(model=r'./yolo11n.pt')

    model.train(data=r'L:\AIProject\AI Labels\EasyYolo\train\trainData_format\data.yaml',
                imgsz=640,
                epochs=10,
                batch=4,
                workers=0,
                device='',
                optimizer='SGD',
                close_mosaic=10,
                resume=False,
                project='runs/train',
                name='exp',
                single_cls=False,
                cache=False,
                )
