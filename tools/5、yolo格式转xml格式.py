# -*- coding: UTF-8 -*-
'''
@Project :AI标注器
@Author  :风吹落叶
@Contack :Waitkey1@outlook.com
@Version :V1.0
@Date    :2025/1/15 11:59
@Describe:
'''
import cv2
import os
from xml.etree.ElementTree import Element, SubElement, ElementTree
from tqdm import tqdm
import shutil
import concurrent.futures
# 函数：将YOLO格式的标注转换为XML格式
def convert_to_xml(img_folder, txt_filepath, xml_filepath, class_mapping):
    # 读取图片尺寸
    img_path = os.path.join(img_folder, os.path.basename(txt_filepath).replace('.txt', '.png'))
    outpath=os.path.join(moveFolder, os.path.basename(txt_filepath).replace('.txt', '.png'))
    image = cv2.imread(img_path)
    if image is None:
        raise FileNotFoundError(f"Image {img_path} not found.")
    if moveimg:
        shutil.copy(img_path, outpath)

    height, width, depth = image.shape

    # 创建XML文件的结构
    annotation = Element('annotation')
    SubElement(annotation, 'folder').text = img_folder
    SubElement(annotation, 'filename').text = os.path.basename(img_path)
    SubElement(annotation, 'path').text = img_path
    source = SubElement(annotation, 'source')
    SubElement(source, 'database').text = 'Unknown'
    size = SubElement(annotation, 'size')
    SubElement(size, 'width').text = str(width)
    SubElement(size, 'height').text = str(height)
    SubElement(size, 'depth').text = str(depth)
    SubElement(annotation, 'segmented').text = '0'

    # 读取YOLO格式的标注文件
    with open(txt_filepath, 'r') as file:
        lines = file.readlines()

    # 对于每个边界框，添加到XML中
    for line in lines:
        class_id, x_center, y_center, bbox_width, bbox_height = map(float, line.split())
        class_name = class_mapping[int(class_id)]

        # 计算边界框的左上角和右下角坐标
        x_min = (x_center - bbox_width / 2) * width
        y_min = (y_center - bbox_height / 2) * height
        x_max = (x_center + bbox_width / 2) * width
        y_max = (y_center + bbox_height / 2) * height

        # 创建XML中的object节点
        obj = SubElement(annotation, 'object')
        SubElement(obj, 'name').text = class_name
        SubElement(obj, 'pose').text = 'Unspecified'
        SubElement(obj, 'truncated').text = '0'
        SubElement(obj, 'difficult').text = '0'
        bbox = SubElement(obj, 'bndbox')
        SubElement(bbox, 'xmin').text = str(int(x_min))
        SubElement(bbox, 'ymin').text = str(int(y_min))
        SubElement(bbox, 'xmax').text = str(int(x_max))
        SubElement(bbox, 'ymax').text = str(int(y_max))

    # 保存XML文件
    tree = ElementTree(annotation)
    tree.write(xml_filepath)

# 类别映射，YOLO的类别ID映射到类名
class_mapping = {
    0: 'person',
    1: 'person_head_face',
    2: 'person_head_no_face'
}
moveimg=True # 是否移动图片
# 图片文件夹路径
img_folder = r'L:\AIProject\datas\imgsTarget_8'
img_folder = r'K:\images_data\images'

# YOLO标注文件路径
labels_folder = r'L:\AIProject\AI Labels\runs\detect\predict32\labels'
xml_dirpath=labels_folder+'_xmls'
moveFolder=labels_folder+'_imgs'
os.makedirs(xml_dirpath, exist_ok=True)
os.makedirs(moveFolder, exist_ok=True)

labels_fileNames= os.listdir(labels_folder)
with concurrent.futures.ThreadPoolExecutor(max_workers=8)as executor:
    futures=[]
    for labels_fileName in labels_fileNames:
        try:
            labelfilepath = os.path.join(labels_folder, labels_fileName)

            # XML文件保存路径
            xml_filepath = os.path.join(xml_dirpath, labels_fileName[:-3] + 'xml')
            if not os.path.exists(xml_filepath):
             # 转换
                futures.append(executor.submit(convert_to_xml, img_folder, labelfilepath, xml_filepath, class_mapping))
                #convert_to_xml(img_folder, labelfilepath, xml_filepath, class_mapping)

        except Exception as e:
            print(e)
    prad=tqdm(total=len(futures))
    for future in concurrent.futures.as_completed(futures):
        prad.update(1)
        future.result()
    prad.close()