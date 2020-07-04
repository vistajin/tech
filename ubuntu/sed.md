### Stream EDitor

```sh
############### display ###############
# 输出第4～7行
sed -n '4,7p' a.txt

# 输出第4行及其后的10行内容，共11行
sed -n '4,+10p' a.txt

# 输出第2,5,7行
sed -n '2p;5p;7p' a.txt

# show line start with This
sed -n '/^This/p' test.txt

# show line contains num
sed -n '/num/p' test.txt

# show line ends with "2."
sed -n '/2.$/p' test.txt

# show odd rows
sed -n 'n;p' test.txt

# show even rows
sed -n 'p;n' test.txt

# show number of lines
sed -n '$=' test.txt

# show line number
sed -n "=;p" vi.md | sed 'N;s/\n/,/'

############ replace ####################
# replace line with row in all lines
sed 's/line/row/g' test.txt

# only replace the 2nd match in each line
sed 's/i/QQQQ/2' test.txt

# only show those changed lines
sed -n 's/number 2/qqqqq/p' test.txt

# save changed lines to out.txt
sed 's/number 2/qqqqq/w out.txt' test.txt

# escape for slash: /bin/sh -> /src/newpath
sed 's/\/bin\/sh/\/src\/newpath/g' test.txt

# suround word with []
echo 'this is a test line' | sed 's/\w\+/[&]/g'
[this] [is] [a] [test] [line]

# 将第4～7行注释掉（行首加#号）
sed '4,7s/^/#/' a.txt

# 删除所有的“xml”、所有的“XML”、所有的字母e，"或"用 \| 来表示
sed 's/xml\|XML\|e//g' a.txt

############### Delete ###################

# delete all lines starts from 2nd line
sed '2,$d' test.txt

# delete all lines
sed 'd' test.txt

# delete 3rd line
sed '3d' test.txt

# delete 1-3 line
sed '1,3d' test.txt
sed '/1/,/3/d' test.txt

# delete 1 and 3 line
sed '1d;3d' test.txt

# delete the last line
sed  '$d' a.txt

# delete empty line, not delete blank line (blank spaces line won't be del)
sed  '/^$/d' a.txt

############### Insert ###################

# insert before 3rd line
sed '3i\
This is an inserted line.' test.txt

# insert 2 lines before 3rd line
sed '3i\
This is an inserted line.\
insert 2nd line' test.txt

# append after 5st line
sed '5a\
This is an inserted line.' test.txt

```


