# -*- coding: UTF-8 -*-
'''
@Project :AI标注器 
@Author  :风吹落叶
@Contack :Waitkey1@outlook.com
@Version :V1.0
@Date    :2025/1/15 14:05 
@Describe:
'''
import cv2
import numpy as np
import os
from imgaug import augmenters as iaa
import imgaug as ia
from tqdm import tqdm
import concurrent.futures
seq = iaa.Sequential([
    iaa.Fliplr(0.5), # 对50%的图像进行左右翻转
    iaa.Affine(
        translate_px={"x": 15, "y": 15}, # 平移
        scale=(0.7, 0.95), # 缩放
    ),
    iaa.Crop(percent=(0, 0.1)), # 裁剪图像
    iaa.Multiply((0.8, 1.3)), # 改变亮度
    iaa.AdditiveGaussianNoise(scale=(1, 15)), # 添加高斯噪声
])
def load_and_augment(image_path, label_path,outimgname, save_dir_images, save_dir_labels):
    # 读取图像
    image = cv2.imread(image_path)
    # 读取对应的标注文件
    with open(label_path, "r") as file:
        lines = file.readlines()

    # 将标注转换为imgaug所需的格式
    bbs = []
    for line in lines:
        class_id, x_center, y_center, width, height = map(float, line.split())
        x1 = (x_center - width / 2) * image.shape[1]
        x2 = (x_center + width / 2) * image.shape[1]
        y1 = (y_center - height / 2) * image.shape[0]
        y2 = (y_center + height / 2) * image.shape[0]
        bbs.append(ia.BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2, label=class_id))

    bbs = ia.BoundingBoxesOnImage(bbs, shape=image.shape)

    # 应用增强
    image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)

    # 保存增强后的图像
    image_aug_path = os.path.join(save_dir_images, outimgname)
    cv2.imwrite(image_aug_path, image_aug)

    # 将增强后的标注转换回YOLO格式并保存
    label_aug_path = os.path.join(save_dir_labels, outimgname[:-3]+'txt')
    with open(label_aug_path, "w") as file:
        for bb in bbs_aug.bounding_boxes:
            x_center = (bb.x1 + bb.x2) / 2 / image_aug.shape[1]
            y_center = (bb.y1 + bb.y2) / 2 / image_aug.shape[0]
            width = (bb.x2 - bb.x1) / image_aug.shape[1]
            height = (bb.y2 - bb.y1) / image_aug.shape[0]
            line = f"{int(bb.label)} {x_center} {y_center} {width} {height}\n"


            if x_center<0 or y_center<0 or width>image_aug.shape[1] or height>image_aug.shape[0]:
                continue

            file.write(line)


def main():
    augmented_images_path="augmented_images2"
    augmented_labels_path="augmented_labels2"
    # 创建增强后的目录
    os.makedirs(augmented_images_path, exist_ok=True)
    os.makedirs(augmented_labels_path, exist_ok=True)

    imgaugNum=4000
    imagePath = "K:\images_data\images"
    labelPath = r"L:\AIProject\AI Labels\runs\detect\predict7\labels"


    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futrues = []
        imgNames = os.listdir(imagePath)
        imgLen=len(imgNames)
        for i in range(imgaugNum):
            # 对数据集中的每个图像应用增强
            image_file = imgNames[i%imgLen]
            outimgname=image_file[:-4]+'_'+str(i)+'.png'
            outpath=os.path.join(augmented_images_path, outimgname)
            if os.path.exists(outpath):
                continue


            image_path = os.path.join(imagePath, image_file)

            label_file = image_file.replace('.jpg', '.txt').replace('.png', '.txt')
            label_path = os.path.join(labelPath, label_file)


            task = executor.submit(load_and_augment, image_path,label_path, outimgname,augmented_images_path, augmented_labels_path)
            futrues.append(task)
        prad = tqdm(total=len(futrues))
        for futrue in concurrent.futures.as_completed(futrues):
            try:
                res = futrue.result()
            except Exception as e:
                print(e)
            prad.update(1)
            # load_and_augment(image_path, label_path, 'augmented_images', 'augmented_labels')

        prad.close()

if __name__ == '__main__':
    main()