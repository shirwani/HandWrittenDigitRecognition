from PIL import Image
from utils import *


if __name__ == '__main__':
    subfolders = get_subfolders(os.getcwd() + '/datasets/images')
    train_X = []
    train_y = []

    cv_X = []
    cv_y = []

    for d in subfolders:
        files = get_files_in_subfolder(d)
        subfolder_name = d.split('/')[-1]
        print(f"Folder: {subfolder_name}")
        i = 0
        for f in files:
            if get_file_extension(f) != '.png':
                continue

            image = Image.open(f)
            Xi = image_to_matrix(image)

            #print(f"Xi.shape: {Xi.shape}")

            i += 1
            if i % 10 == 0:
                cv_X.append(Xi)
                cv_y.append([int(subfolder_name)])
            else:
                train_X.append(Xi)
                train_y.append([int(subfolder_name)])


    np.save('datasets/train_X.npy', np.array(train_X))
    np.save('datasets/train_y.npy', np.array(train_y))

    np.save('datasets/cv_X.npy', np.array(cv_X))
    np.save('datasets/cv_y.npy', np.array(cv_y))

