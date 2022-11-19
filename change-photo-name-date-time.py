# Change photo name by photo date/time and vice versa.
# 功能：
# 1. 根据照片名称修改照片日期：根据照片名中包含的日期信息，修改照片Exif中的日期信息
# 2. 根据照片日期修改照片名称：根据照片Exif中的日期信息，按照统一格式重命名照片

import os, time, piexif, re
import re
from PIL import Image

# ------------------------------------------------------------------
## general functions
# ------------------------------------------------------------------
def check_format(photo_path):
    '''
    检查文件类型是否为图片格式，返回文件后缀类型，大写字母
    '''
    return str.upper(os.path.splitext(photo_path)[1][1:])


def check_exif(photo_path):
    '''
    检查文件是否有Exif，Exif中是否有拍摄时间
    '''
    try:
        exif_dict = piexif.load(photo_path)  # 读取Exif信息
        return piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif']
    except:
        return False


def png2jpg(photo_path):
    '''
    png2jpg
    ps. 直接改文件后缀名，后续跑不通，piexif不认这个JPG，原因不详
    '''
    print('  Executing png2jpg')
    new_photo_path = os.path.splitext(photo_path)[0] + '.jpg'  # 改后缀类型
    Image.open(photo_path).convert('RGB').save(new_photo_path, quality=95)
    os.remove(photo_path)
    return new_photo_path


# ------------------------------------------------------------------
## change photo name based on photo time
# ------------------------------------------------------------------
def change_photo_name(folder):
    '''
    修改JPG照片的文件名为拍摄日期，如果Exif中不包含拍摄日期，修改文件名为照片修改日期
    e.g., IMG_20210424_071829.jpg
    '''
    count = 0
    file_num = len(os.listdir(folder))
    for photo_name in os.listdir(folder):
        print(f'{file_num - count} Working on file: {photo_name}') # 显示处理进度
        count += 1
        photo_path = os.path.join(folder, photo_name)  # 照片的绝对路径
        if check_format(photo_path) == 'PNG': photo_path = png2jpg(photo_path)
        if check_format(photo_path) in ['JPG', 'JPEG']:
            if check_exif(photo_path):  # 是JPG且Exif包含时间信息
                photo_time = get_time_from_exif(photo_path)
            else:  # Exif中不包含拍摄日期，修改文件名为照片修改日期 
                photo_time = get_time_from_create_date(photo_path)
                no_exif.append(photo_name)
                print(f'  No Exif, photo name has been changed to create date')
            photo_name, temp_photo_path = get_new_name(photo_path, photo_time)
            new_photo_path = os.path.join(folder, photo_name)
            os.rename(temp_photo_path, new_photo_path)
            print(f'  Done, photo name has been changed to {photo_name}\n')
        else:
            print(f'  Not JPG file, end process\n')


def get_time_from_exif(photo_path):
    '''
    从Exif中提取照片时间，返回格式为2021:04:22 07:07:07
    '''
    exif_dict = piexif.load(photo_path)  # 照片的Exif
    photo_time = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]  # bytes
    photo_time = bytes.decode(photo_time)  # 解码后为2021:04:22 07:07:07
    return photo_time

def get_time_from_create_date(photo_path):
    '''
    从照片修改日期提取时间，返回格式为2021:04:22 07:07:07
    '''
    photo_time = time.ctime(os.path.getmtime(photo_path)) # 如果使用修改日期，则改为os.path.getmtime()
    struct_time = time.strptime(photo_time, '%a %b %d %H:%M:%S %Y')
    photo_time = time.strftime('%Y:%m:%d %H:%M:%S', struct_time)
    return photo_time  


def get_new_name(photo_path, photo_time):
    '''
    获取照片新文件名，如果两张照片时分秒也相同，在文件名后累加数字1 2 3...区分
    e.g., IMG_20210422_070707_X.jpg
    '''
    count = 1
    temp_photo_name = 'bcwyatt.jpg'  # 使用临时文件名，避免重复在后面加_1_1
    temp_photo_path = os.path.join(folder, temp_photo_name)
    os.rename(photo_path, temp_photo_path)
    photo_time = photo_time.replace(':', '').replace(' ', '_')
    photo_name = f'IMG_{photo_time}.jpg' # 生成照片新文件名
    while photo_name in os.listdir(folder): # 区分时间相同的文件名
        photo_name = f'IMG_{photo_time}_{count}.jpg'
        count += 1
    return photo_name, temp_photo_path


# ------------------------------------------------------------------
## change photo time based on photo name
# ------------------------------------------------------------------
def change_photo_time(folder):
    '''
    修改该路径下的所有JPG照片的时间
    '''
    count = 0
    file_num = len(os.listdir(folder))
    for photo_name in os.listdir(folder):
        # 展示剩余文件数量 + 正在处理的文件名
        print(f'{file_num - count} Working on file: {photo_name}')
        count += 1
        photo_path = os.path.join(folder, photo_name)  # 照片的绝对路径
        if check_format(photo_path) == 'PNG': 
            photo_path = png2jpg(photo_path)
        if check_format(photo_path) in ['JPG', 'JPEG']:
            set_photo_time(photo_name, photo_path)
        else:
            print('  Not JPG file, end process\n')


def get_time_from_name(photo_name):
    '''
    利用正则表达式从文件名中提取时间，再转换为Exif时间格式
    from 'IMG_20220102_030405.jpg' to '2022:01:01 03:04:05'
    '''
    pn = photo_name
    # 文件名包含年月日时分秒，无分隔符或分隔符为（-._/）四种之一，如'2022.08.08_07/58/10.jpg'
    pattern_1 = re.compile(r'\d{4}([-|.|/|_]?\d{2}){5}')
    pattern_2 = re.compile(r'\d{10}')  # 文件名包含时间戳，如'mmexport1569824283462.jpg'

    if pattern_1.search(pn):  # 满足pattern_1，文件名包含年月日时分秒
        pn = pattern_1.search(pn).group()
        pn = pn.replace('_', '').replace('-', '').replace('.', '').replace('/', '')
        photo_time = f'{pn[0:4]}:{pn[4:6]}:{pn[6:8]} {pn[8:10]}:{pn[10:12]}:{pn[12:14]}'
    elif pattern_2.search(pn):  # 满足pattern_2，文件名包含时间戳
        pn = pattern_2.search(pn).group()
        photo_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(int(pn)))
    elif check_exif(os.path.join(folder, photo_name)):  # 文件名中没有时间，但Exif中有时间
        photo_time = get_time_from_exif(os.path.join(folder, photo_name))
        no_time_in_name.append(photo_name)
        print('  No time in name, photo_time has been extracted from Exif')
    else:  # 文件名和Exif中都没有时间信息，则设置照片时间为照片修改日期
        photo_time = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime())
        photo_time = get_time_from_create_date(os.path.join(folder, photo_name))
        no_time_in_name.append(photo_name)
        print('  No time in name and Exif, photo_time has been changed to create date')
    return photo_time


def set_photo_time(photo_name, photo_path):
    '''
    给照片设置拍摄时间，导入exif信息
    '''
    photo_time = get_time_from_name(photo_name)  # 格式为'2024:04:22 07:58:10'
    try:
        exif_dict = piexif.load(photo_path)  # 读取现有Exif信息
        # 设置Exif信息，注意DateTime在ImageIFD里面
        exif_dict['0th'][piexif.ImageIFD.DateTime] = photo_time  
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = photo_time
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = photo_time
        try:
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, photo_path)  # 插入Exif信息
            print(f'  Done, photo time has been changed to {photo_time}')
        except:
            print(f'  Exif dump error')
    except:
        exif_load_error.append(photo_name)
        print('  Exif load error')
    
    # 修改文件的修改日期和访问日期
    try:
        mod_time = time.mktime(time.strptime(photo_time, '%Y:%m:%d %H:%M:%S'))
        os.utime(photo_path, (mod_time, mod_time))  # 想修改创建日期可能需要win32库
        print(f'  Done, photo_mod_time has been changed to {photo_time}\n')
    except:
        print(f'  No time in name, cannot change photo_mod_time\n')

# ------------------------------------------------------------------
## main
# ------------------------------------------------------------------
if __name__ == '__main__':
    '''
    folder: 需要修改的照片文件夹路径
    '''
    folder = r'D:\4 照片\新建文件夹\新建文件夹'  # 此处改为需要修改的照片文件夹路径
    no_exif, exif_load_error, no_time_in_name = [[] for i in range(3)]

    motion = input('Change name or time: ') # 输入需要修改照片name还是time
    while motion not in ['name', 'time']:
        motion = input('Please just input name or time: ')
    if motion == 'name':
        change_photo_name(folder)
    else:  # motion == 'time'
        change_photo_time(folder)
    
    # 统计不能执行的照片文件
    if no_exif: 
        print('Photos_no_exif:\n', no_exif)
    if exif_load_error: 
        print('Photos_exif_load_error:\n', exif_load_error)
    if no_time_in_name: 
        print('Photos_no_time_in_name:\n', no_time_in_name)