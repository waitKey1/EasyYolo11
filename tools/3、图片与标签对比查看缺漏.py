# -*- coding: UTF-8 -*-
'''
@Project :AI标注器 
@Author  :风吹落叶
@Contack :Waitkey1@outlook.com
@Version :V1.0
@Date    :2025/1/15 12:21 
@Describe:
'''
import os

# 设置文件夹路径
folder_a =r'L:\AIProject\AI标注器\runs\detect\predict7\labels'
folder_b = 'K:\images_data\images'
folder_a_files=os.listdir(folder_a)
folder_a_files=[file[:-4] for file in folder_a_files ]

folder_b_files=os.listdir(folder_b)
folder_b_files=[file[:-4] for file in folder_b_files ]

# 读取两个文件夹内的文件名
files_in_a = set(folder_a_files)
files_in_b = set(folder_b_files)

# 检查两个文件夹的文件名是否一致
if files_in_a == files_in_b:
    print("文件夹A和文件夹B内的文件名一致。")
else:
    print("文件夹A和文件夹B内的文件名不一致。")

# 找出存在于文件夹A但不存在于文件夹B的文件
diff_files =  files_in_b - files_in_a

# 如果有存在于A但不在B的文件，导出它们的列表
if diff_files:
    print(f"存在于文件夹A但不存在于文件夹B的文件有：{diff_files}")
    # 导出文件名到文本文件
    with open('diff_files.txt', 'w') as f:
        for file in diff_files:
            f.write(file + '\n')
    print("这些文件名已经被写入到diff_files.txt文件中。")
else:
    print("没有文件仅存在于文件夹A中。")
