import os
import glob
import random
import string

def get_random_string():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

def rename_files(digit):
    l = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    imgdir = './datasets/images/' + str(digit)
    pre = l[digit]
    image_files = glob.glob(os.path.join(imgdir, '*.png'), recursive=False)

    for f in image_files:
        orgfilename = os.path.basename(f)
        file_extension = os.path.splitext(f)[1]
        newfilename = pre + '_' + get_random_string() + file_extension

        org_file = os.path.join(imgdir, orgfilename)
        new_file = os.path.join(imgdir, newfilename)

        print(org_file + ' --> ' + new_file)
        os.rename(org_file, new_file)


def count_files(digit):
    imgdir = './datasets/images/' + str(digit)
    image_files = glob.glob(os.path.join(imgdir, '*.png'), recursive=False)

    print(f"{digit}: {len(image_files)}")


if __name__ == '__main__':

    for i in range(10):
        rename_files(i)

    for i in range(10):
        count_files(i)



