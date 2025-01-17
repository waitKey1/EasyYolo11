# -*- coding: UTF-8 -*-
'''
@Project :AIProject 
@Author  :风吹落叶
@Contack :Waitkey1@outlook.com
@Version :V1.0
@Date    :2025/1/15 10:51 
@Describe:
'''
import os, shutil
from sklearn.model_selection import train_test_split


val_size = 0.3
#test_size = 0.2
postfix = 'png'
dirpath = r'L:\AIProject\AI Labels\EasyYolo\train\trainData'
trainDataset=dirpath+'_format'
os.makedirs(trainDataset, exist_ok=True)
# 获取文件名
filedir = os.listdir(dirpath)
for file in filedir:
    if file.startswith(('im')):
        imgpath =os.path.join(dirpath, file)
    if file.startswith(('la')):
        txtpath = os.path.join(dirpath, file)


# 创建文件夹
output_train_img_folder = os.path.join(trainDataset,'train','images')
output_train_txt_folder = os.path.join(trainDataset,'train','labels')

output_val_img_folder = os.path.join(trainDataset,'val','images')
output_val_txt_folder = os.path.join(trainDataset,'val','labels')

trainYaml=os.path.join(trainDataset,'data.yaml')

with open(trainYaml,'w',encoding='utf-8') as f:
    trainpath=os.path.join(trainDataset,'train')
    valpath=os.path.join(trainDataset,'val')
    f.write(f'train : {trainpath}\n')
    f.write(f'val : {trainpath}\n')
    f.write(f'nc: 3\n')
    f.write(f"names: ['person','person_head_face','person_head_no_face']\n")


os.makedirs(output_train_img_folder, exist_ok=True)
os.makedirs(output_val_img_folder, exist_ok=True)
os.makedirs(output_train_txt_folder, exist_ok=True)
os.makedirs(output_val_txt_folder, exist_ok=True)


listdir = [i for i in os.listdir(txtpath) if 'txt' in i]
train, val = train_test_split(listdir, test_size=val_size, shuffle=True, random_state=0)

#todo：需要test放开

# train, test = train_test_split(listdir, test_size=test_size, shuffle=True, random_state=0)
# train, val = train_test_split(train, test_size=val_size, shuffle=True, random_state=0)

for i in train:
    img_source_path = os.path.join(imgpath, '{}.{}'.format(i[:-4], postfix))
    txt_source_path = os.path.join(txtpath, i)

    img_destination_path = os.path.join(output_train_img_folder, '{}.{}'.format(i[:-4], postfix))
    txt_destination_path = os.path.join(output_train_txt_folder, i)

    shutil.copy(img_source_path, img_destination_path)
    shutil.copy(txt_source_path, txt_destination_path)

for i in val:
    img_source_path = os.path.join(imgpath, '{}.{}'.format(i[:-4], postfix))
    txt_source_path = os.path.join(txtpath, i)

    img_destination_path = os.path.join(output_val_img_folder, '{}.{}'.format(i[:-4], postfix))
    txt_destination_path = os.path.join(output_val_txt_folder, i)

    shutil.copy(img_source_path, img_destination_path)
    shutil.copy(txt_source_path, txt_destination_path)


#
# for i in train:
#     shutil.copy('{}/{}.{}'.format(imgpath, i[:-4], postfix), r'E:\1-cheng\4-yolo-dataset-daizuo\multi-classify\bird-boat-horse-aeroplane-sheep\dataset20231219/images/train/{}.{}'.format(i[:-4], postfix))
#     shutil.copy('{}/{}'.format(txtpath, i), r'E:\1-cheng\4-yolo-dataset-daizuo\multi-classify\bird-boat-horse-aeroplane-sheep\dataset20231219/labels/train/{}'.format(i))
#
# for i in val:
#     shutil.copy('{}/{}.{}'.format(imgpath, i[:-4], postfix), r'E:\1-cheng\4-yolo-dataset-daizuo\multi-classify\bird-boat-horse-aeroplane-sheep\dataset20231219/images/val/{}.{}'.format(i[:-4], postfix))
#     shutil.copy('{}/{}'.format(txtpath, i), r'E:\1-cheng\4-yolo-dataset-daizuo\multi-classify\bird-boat-horse-aeroplane-sheep\dataset20231219/labels/val/{}'.format(i))

#todo:需要test则放开

# for i in test:
#     shutil.copy('{}/{}.{}'.format(imgpath, i[:-4], postfix), 'images/test/{}.{}'.format(i[:-4], postfix))
#     shutil.copy('{}/{}'.format(txtpath, i), 'labels/test/{}'.format(i))
