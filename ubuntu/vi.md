

```sh
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
```

