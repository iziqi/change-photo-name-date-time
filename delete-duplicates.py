# 删除同名的JPG图片，保留HEIC图片

import os


def check_format(photoPwd):
    """
    检查文件类型
    """
    return str.upper(os.path.splitext(photoPwd)[1][1:])  # 返回文件类型


def del_duplicate(folder):
    """
    删除同名的JPG图片，保留HEIC图片
    """
    photos = os.listdir(folder)
    for photo in photos:
        photo_pwd = os.path.join(folder, photo)  # 照片的绝对路径
        photo_name = os.path.splitext(photo)[0]
        dup_exist = photo_name + ".jpg" in photos or photo_name + ".JPG" in photos
        if check_format(photo_pwd) == "HEIC" and dup_exist:  # 如果照片为heic格式，并且有同名的jpg文件，删除之
            os.remove(os.path.splitext(photo_pwd)[0] + ".jpg")
            print(photo_name + ".jpg " + "has been deleted")


## Main
if __name__ == "__main__":
    """
    folder: 文件夹路径
    """
    folder = r"D:\4 照片\新建文件夹\新建文件夹"
    del_duplicate(folder)
