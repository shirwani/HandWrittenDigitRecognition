import numpy as np
import os
from PIL import Image


def image_to_matrix(image_path):
    image = Image.open(image_path)
    img_array = np.array(image)
    if len(img_array.shape) == 3:
        img_array = np.mean(img_array, axis=-1)

    img_array = img_array / 255.0
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


if __name__ == '__main__':
    subfolders = get_subfolders(os.getcwd() + '/training_images')
    X = []
    y = []

    for d in subfolders:
        files = get_files_in_subfolder(d)
        subfolder_name = d.split('/')[-1]
        print(subfolder_name)
        for f in files:
            if get_file_extension(f) != '.png':
                continue
            img_array = image_to_matrix(f)
            Xi = img_array.reshape(10000)
            X.append(Xi)
            y.append([int(subfolder_name)])

    X = np.array(X)
    Y = np.array(y)

    np.save('training_data/X.npy', X)
    np.save('training_data/y.npy', y)

