# 之前日记记录在Onenote里面，现在想要迁移到其他md笔记管理软件
# 需要批量将Onenote笔记分区导出的docx文件按照一定格式要求转换为md文件

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


def tem_md2new_md(tmp_note, new_note):
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
    p1 = re.compile(r'^\s*\d{1,2}月\s*$') # 1月 → # 1月\n\n
    p2 = re.compile(r'^\s*\d{1,2}\.\d{1,2}\s*$') # 1.1 → ## 1.1\n\n
    p3 = re.compile(r'[\u4E00-\u9FA5]+') # 中文段落 → 段落\n\n # 这个也会匹配2021年1月1日，p4要在p3前面
    p4 = re.compile(r'^\d{4}年\d{1,2}月\d{1,2}日') # 2021年1月1日 → delete
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


def split_md(tmp_note):
    '''
    按照一级标题分割文件
    '''

    # 正则表达式
    p1 = re.compile(r'^#.*') # # XXXXX 一级标题
    p2 = re.compile(r'^##.*') # ## XXXXX 二级标题
    p3 = re.compile(r'.', re.DOTALL) # 匹配正文 匹配所有内容

    # 按照一级标题分割文件
    with open(tmp_note,'r',encoding='utf-8') as f:
        for line in f: 
            print(line)
            if p1.search(line):
                tmp_folder = line.split(' ')[1] # 提取一级标题名称作为文件夹名称
                if not os.path.exists(tmp_folder): os.makedirs(tmp_folder)
                with open(new_note,'a', encoding='utf-8') as f:
                    f.write(tmp_note_text)
            elif p2.search(line):
                tmp_note_name = line.split(' ')[1] # 提取二级标题名称作为md文件名

                new_note = os.path.join(tmp_folder, tmp_note_name + '.md')
                tmp_note_text = ''
            elif p3.search(line):
                tmp_note_text += line

            new_note_txt += line
            with open(new_note,'a', encoding='utf-8') as f2:
                f2.write(line)

# ------------------------------------------------------------------
## main
# ------------------------------------------------------------------
if __name__ == '__main__':
    '''
    批量将Onenote笔记分区导出的docx文件按照一定格式要求转换为md文件
    '''

    # 初始化notes文件夹
    old_notes_folder = 'onenote-notes' # Onenote导出的word文件放在这里
    tmp_notes_folder = 'md-tmp-notes'
    new_notes_folder = 'md-notes'

    old_notes_folder = os.path.join(os.getcwd(), old_notes_folder)
    tmp_notes_folder = os.path.join(os.getcwd(), tmp_notes_folder)
    new_notes_folder = os.path.join(os.getcwd(), new_notes_folder)

    shutil.rmtree(new_notes_folder, ignore_errors=True) # 清空目标文件夹，包括文件夹本身
    shutil.rmtree(tmp_notes_folder, ignore_errors=True) 
    if not os.path.exists(tmp_notes_folder): os.makedirs(tmp_notes_folder)
    if not os.path.exists(new_notes_folder): os.makedirs(new_notes_folder)

    # transfer from onenote-docx to markdown
    for note in os.listdir(old_notes_folder):
        print(f'Working on file: {note}') # 显示处理进度

        note_name = str(os.path.splitext(note)[0])
        old_note = os.path.join(old_notes_folder, note)
        tmp_note = os.path.join(tmp_notes_folder, note_name + '_tmp.md')
        new_note = os.path.join(new_notes_folder, note_name + '.md')

        tmp_note = word2tmp_md(old_note, tmp_note, new_notes_folder)
        new_md = tem_md2new_md(tmp_note, new_note)
