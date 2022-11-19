# 之前日记记录在Onenote里面，现在想要迁移到其他md笔记管理软件
# 每年的日记为一个Onenote分区，可以导出为docx文件
# word2tmp_md：提取docx文件中的文本并储存为md文件
# tmp_md2new_md：将提取的文本内容格式化，设置一二级标题等等
# split_md：分割每年的日记，每月一个文件夹，每天的日记单独一个md文件

import re, os
import docx2txt
import shutil

def word2tmp_md(old_note, tmp_note, new_notes_folder):
    '''
    extract text from word file and save images in \img_folder
    '''
    img_folder = os.path.join(new_notes_folder, 'img_folder')
    if not os.path.exists(img_folder): os.makedirs(img_folder)
    text = docx2txt.process(old_note, img_folder)
    with open(tmp_note,'a',encoding='utf-8') as f:
        f.write(text)
    return tmp_note


def tmp_md2new_md(tmp_note, new_note):
    '''
    transfer text from tmp_md to final_md
    format the text with following rules
        1月 → # 1月\n\n
        1.1 → ## 1.1\n\n
        中文段落 → 段落\n\n
        2021年1月1日 → delete
        23:10 → delete
        空行 → delete
    '''
    # 正则表达式
    p1 = re.compile(r'^\s*\w*月\s*$') # XX月 → # XX月\n\n
    p2 = re.compile(r'^\s*\d{1,2}\.\d{1,2}\s*$') # 1.1 → ## 1.1\n\n
    p3 = re.compile(r'[\u4E00-\u9FA5]+') # 中文段落 → 段落\n\n # 这个也会匹配2021年1月1日，p4要在p3前面
    p4 = re.compile(r'^\d{4}年\d{1,2}月\d{1,2}日$') # 2021年1月1日 → delete
    p5 = re.compile(r'^\d{1,2}:\d{1,2}$') # 23:10 → delete
    p6 = re.compile(r'.', re.DOTALL) # 空行 → delete

    with open(tmp_note,'r',encoding='utf-8') as f:
        new_note_txt = ''
        for line in f: 
            if p4.search(line) or p5.search(line):
                line = ''
            elif p1.search(line):
                line = '# ' + line.strip() + '\n\n' #需要两个换行符
            elif p2.search(line):
                line = '## ' + line.strip() + '\n\n'
            elif p3.search(line):
                line = line.strip() + '\n\n'
            elif p6.search(line): # 匹配换行，这个必须放最后
                line = ''
            new_note_txt += line
    with open(new_note,'a', encoding='utf-8') as f:
        f.write(new_note_txt)
    return new_note


def split_md(note_to_be_splited, new_notes_folder):
    '''
    按照分级标题分割文件
    一级标题为文件夹，二级标题段落为该文件夹下的单独md文件
    '''
    # 正则表达式
    p1 = re.compile(r'^#\s.+$') # # XXXXX 一级标题
    p2 = re.compile(r'^##\s.+$') # ## XXXXX 二级标题
    p3 = re.compile(r'.', re.DOTALL) # 匹配正文和换行 匹配所有内容

    # 按照分级标题分割文件，一级标题为文件夹，二级标题段落为该文件夹下的单独md文件
    # 每个二级标题段落后面有三种可能：下个一级标题，下个二级标题，文件结尾
    with open(note_to_be_splited,'r',encoding='utf-8') as f:
        count = 0
        for line in f: 
            if p1.search(line):
                if count != 0: # 排除第一次经过，处理后续一级标题前的那个二级标题
                    with open(separate_note,'a', encoding='utf-8') as f:
                        f.write(tmp_note_text)
                tmp_folder_name = line.split(' ')[1].replace('\n', '') # 提取一级标题作为文件夹名
                tmp_folder = os.path.join(new_notes_folder, tmp_folder_name)
                shutil.rmtree(tmp_folder, ignore_errors=True) # 清空目标文件夹，包括文件夹本身
                if not os.path.exists(tmp_folder): os.makedirs(tmp_folder)
            elif p2.search(line):
                if count != 0: # 排除第一次经过
                    with open(separate_note,'a', encoding='utf-8') as f:
                        f.write(tmp_note_text)
                count += 1
                separate_note_name = line.split(' ')[1].replace('\n', '') # 提取二级标题为md文件名
                separate_note = os.path.join(tmp_folder, separate_note_name + '.md')
                tmp_note_text = '# ' + separate_note_name + '\n' # 二级标题名称作为md开头
            elif p3.search(line):
                if count != 0:
                    tmp_note_text += line
        if count != 0: # 处理文件结尾的最后一个二级标题
            with open(separate_note,'a', encoding='utf-8') as f:
                f.write(tmp_note_text)

# ------------------------------------------------------------------
## main
# ------------------------------------------------------------------
if __name__ == '__main__':
    '''
    批量将Onenote笔记分区导出的docx文件按照一定格式要求转换为md文件
    '''

    # 初始化notes文件夹
    old_notes_folder = os.path.join(os.getcwd(), 'docx_notes') # Onenote导出的word文件放在这里
    tmp_notes_folder = os.path.join(os.getcwd(), 'tmp_md_notes')
    new_notes_folder = os.path.join(os.getcwd(), 'new_md_notes') # 最终的md文件都在这里

    shutil.rmtree(new_notes_folder, ignore_errors=True) # 清空目标文件夹，包括文件夹本身
    shutil.rmtree(tmp_notes_folder, ignore_errors=True) 
    if not os.path.exists(tmp_notes_folder): os.makedirs(tmp_notes_folder)
    if not os.path.exists(new_notes_folder): os.makedirs(new_notes_folder)

    # transfer from onenote-docx to markdown
    for note in os.listdir(old_notes_folder):
        print(f'Working on file: {note}') # 显示处理进度

        note_name = str(os.path.splitext(note)[0]) # YYYY 年份
        old_note = os.path.join(old_notes_folder, note)
        tmp_note = os.path.join(tmp_notes_folder, note_name + '_tmp.md')
        new_note = os.path.join(new_notes_folder, note_name + '.md')

        # 提取docx文件中的文本并储存为md文件
        tmp_note = word2tmp_md(old_note, tmp_note, new_notes_folder)

        # 将提取的文本内容格式化，设置一二级标题等等
        new_note = tmp_md2new_md(tmp_note, new_note)

        # 分割每年的日记，每月一个文件夹，每天的日记单独一个md文件
        separate_notes_folder = os.path.join(new_notes_folder, note_name)
        shutil.rmtree(separate_notes_folder, ignore_errors=True)
        if not os.path.exists(separate_notes_folder): os.makedirs(separate_notes_folder)
        split_md(new_note, separate_notes_folder)