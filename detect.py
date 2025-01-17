# -*- coding: UTF-8 -*-
'''
@Project :AI标注器 
@Author  :风吹落叶
@Contack :Waitkey1@outlook.com
@Version :V1.0
@Date    :2025/1/15 11:52 
@Describe:
'''
import os

from ultralytics import YOLO

if __name__ == '__main__':
    dirpath=r'./testimgs'
    # Load a model
    model = YOLO(model=r'L:\AIProject\AI Labels\EasyYolo\train\runs\train\exp4\weights\best.pt')
    res = model.predict(source=dirpath,
                        # save=True,
                        # show=True,
                        save_txt=True
                        )


    #model.predict(source=r'K:\images_data\lossImgs',
