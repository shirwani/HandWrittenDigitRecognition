import numpy as np
import os
import json
from datetime import datetime

def get_configs():
    with open('config.json', 'r') as cfgfile:
        cfg = json.load(cfgfile)
    return cfg

def image_to_matrix(image):
    img_array = np.array(image) # convert image to np.array()
    # print(f"image_array.shape -> {img_array.shape}")

    if len(img_array.shape) == 3:
        img_array = np.mean(img_array, axis=-1)

    img_array = img_array / 255.0 # scaling it so the value is between 0 and 1
    img_array = img_array.reshape(10000) # convert image array to a column vector -> (10000,)
    return img_array


def get_subfolders(directory):
    subfolders = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    return subfolders


def get_files_in_subfolder(subfolder_path):
    files = [f.path for f in os.scandir(subfolder_path) if f.is_file()]
    return files


def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension


def get_date_time_str():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
