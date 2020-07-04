





```sh
# 打开文件，并将光标置于第n行首 
vi +n filename
# 打开文件，并将光标置于最后一行首 
vi + filename
# 打开文件，并将光标置于第一个与pattern匹配的串处 
vi +/pattern filename
# 在上次正用vi编辑时发生系统崩溃，恢复filename 
vi -r filename
# 打开多个文件，依次进行编辑
vi filename....filename

# 进入编辑模式： 
i
o - 新插入一行
O
a
A

# 翻页 （只读下）
ctrl F, ctrl B

gg - 起始位置
G - 底部

xG - 跳到第x行
:x - 跳到第x行

:set number - 显示行号
:set nu - 显示行号

u - 撤销，相当于ctrl z

xdd - 删除光标开始的x行

yy + p - yy复制当前行，p粘贴复制到的行

# vi replace sample
:%s/Answer: [A-Q]*/Answer: X/g

# 将当前行中所有p1均用p2替代 
sp1/p2/g
# 将第n1至n2行中所有p1均用p2替代 
n1,n2s/p1/p2/g
# 将文件中所有p1均用p2替换
g/p1/s//p2/g
```

# 保存并退出，相当于:x
shift + zz

# 查找时大小写敏感切换
set ic
set noic

