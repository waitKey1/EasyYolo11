# -*- coding: UTF-8 -*-
'''
@Project :AIProject 
@Author  :风吹落叶
@Contack :Waitkey1@outlook.com
@Version :V1.0
@Date    :2025/1/15 10:46 
@Describe:
'''
import os
import zipfile

# Directory containing the zip files
source_dir = '/datas2'  # Replace with your source folder path
# Directory where the zip files will be extracted
extract_dir = source_dir+'extr'  # Replace with your target folder path

if not os.path.exists(extract_dir):
    os.makedirs(extract_dir)

# Iterate through all ZIP files in the source directory
for file_name in os.listdir(source_dir):
    if file_name.endswith('.zip'):
        zip_path = os.path.join(source_dir, file_name)
        subfolder_name = os.path.splitext(file_name)[0]  # Use the zip file name (without extension) as subfolder
        subfolder_path = os.path.join(extract_dir, subfolder_name)

        # Create the subfolder
        os.makedirs(subfolder_path, exist_ok=True)

        # Extract the contents of the zip file into the subfolder
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(subfolder_path)
            print(f"Extracted {file_name} to {subfolder_path}")
        except zipfile.BadZipFile:
            print(f"Error: {file_name} is not a valid zip file.")
        except Exception as e:
            print(f"An error occurred while processing {file_name}: {e}")