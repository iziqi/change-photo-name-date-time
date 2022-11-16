# 需要处理的文本内容
# 1月 → # 1月\n\n
# 1.1 → ## 1.1\n\n
# 中文段落 → 段落\n\n
# 2021年1月1日 → delete
# 23:10 → delete
# 空行 → delete

import re, os
import docx2txt
import shutil

# 初始化notes文件夹
old_notes_folder = 'onenote-notes'
tmp_notes_folder = 'md-tmp-notes'
new_notes_folder = 'md-notes'

old_notes_folder = os.path.join(os.getcwd(), old_notes_folder)
tmp_notes_folder = os.path.join(os.getcwd(), tmp_notes_folder)
new_notes_folder = os.path.join(os.getcwd(), new_notes_folder)

shutil.rmtree(new_notes_folder, ignore_errors=True) # 清空目标文件夹
shutil.rmtree(tmp_notes_folder, ignore_errors=True) 
os.makedirs(new_notes_folder)
os.makedirs(tmp_notes_folder)

# 正则表达式
p1 = re.compile(r'^\s*\d{1,2}月\s*$') # 1月 → # 1月\n\n
p2 = re.compile(r'^\s*\d{1,2}\.\d{1,2}\s*$') # 1.1 → ## 1.1\n\n
p3 = re.compile(r'[\u4E00-\u9FA5]+') # 中文段落 → 段落\n\n # 这个也会匹配2021年1月1日，p4要在p3前面
p4 = re.compile(r'^\d{4}年\d{1,2}月\d{1,2}日') # 2021年1月1日 → delete
p5 = re.compile(r'^\d{1,2}:\d{1,2}$') # 23:10 → delete
p6 = re.compile(r'.', re.DOTALL) # 空行 → delete

# transfer from onenote-docx to markdown
for note in os.listdir(old_notes_folder):
    print(f'Working on file: {note}') # 显示处理进度

    note_name = str(os.path.splitext(note)[0])
    
    old_note = os.path.join(old_notes_folder, note)
    tmp_note = os.path.join(tmp_notes_folder, note_name + '_tmp.md')
    new_note = os.path.join(new_notes_folder, note_name + '.md')

    # extract text from word file and save images in \img_folder
    img_folder = os.path.join(new_notes_folder, 'img_folder')
    if not os.path.exists(img_folder): os.makedirs(img_folder)
    text = docx2txt.process(old_note, img_folder)
    with open(tmp_note,'a',encoding='utf-8') as f:
        f.write(text)

    # transfer text from tmp_notes-md to final_markdown_file
    with open(tmp_note,'r',encoding='utf-8') as f1:
        for line in f1: 
            # print(line)
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
            # print(line)
            with open(new_note,'a', encoding='utf-8') as f2:
                f2.write(line)

shutil.rmtree(tmp_note, ignore_errors=True) 
shutil.rmtree(img_folder, ignore_errors=True) 
