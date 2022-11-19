# transfer-notes-onenote2md

一直在Onenote里面记日记，现在想要迁移到其他md笔记管理软件。

根据我之前的习惯，每年的日记为一个Onenote分区，可以导出为docx文件

![IMG_202211191436262](https://img-1313032483.cos.ap-beijing.myqcloud.com/202211191436262.webp)

导出的docx文件里面不包含标题样式，用这个脚本正则匹配“X月”“X.XX”，分别设置为一二级标题。


word2tmp_md：提取docx文件中的文本并储存为md文件

tmp_md2new_md：将提取的文本内容格式化，设置一二级标题等等

split_md：分割每年的日记，每月一个文件夹，每天的日记单独一个md文件
