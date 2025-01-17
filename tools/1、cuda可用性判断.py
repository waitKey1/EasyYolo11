# -*- coding: UTF-8 -*-
'''
@Project :AI标注器 
@Author  :风吹落叶
@Contack :Waitkey1@outlook.com
@Version :V1.0
@Date    :2025/1/15 9:07 
@Describe:
'''
import torch

if torch.cuda.is_available():
    print("CUDA is available")
else:
    print("CUDA is not available")
