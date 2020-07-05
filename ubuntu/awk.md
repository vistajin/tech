http://www.gnu.org/software/gawk/manual/gawk.html

内置函数列表：https://www.gnu.org/software/gawk/manual/html_node/Built_002din.html#Built_002din

```sh
# 开始和结束
awk 'BEGIN{}END{}'

echo -e "A line 1\nA line 2" | awk 'BEGIN{print "Start"} {print} END{print "end"}'

# 多分割符 / : , 都是分隔符
awk -F "[/:,]"

# 正则匹配
awk '/Running/'
# 区间选择
awk '/aa/,/bb/'
# 字段匹配，这里指从第二个字段开始
awk '$2/xxx/'
# 取第二行
awk 'NR==2'
# 去掉第一行
awk 'NR>1'
#只查看test.txt文件第20到第30行的内容
awk '{if(NR>=20 && NR<=30) print $1}' test.txt

# 计算文件大小
ll | awk '{sum+=$5} END {print sum}'

# 找出长度大于80的行
awk 'length>80' log.txt

ll | awk '{print $9}'

echo "1-2-3-4" | awk -F- '{print $3}'

awk -F: '{printf ("filename:%10s, linenumber:%3s,column:%3s,content:%3f\n",FILENAME,NR,NF,$0)}' /etc/passwd

# $NF 最后一个字段，$(NF-1)倒数第二个字段， NF 字段的数量
echo 'this is a test' | awk '{print $NF}'  # 输出test
echo 'this is a test' | awk '{print NF}'    # 输出 4

# 输出加“,”表示用空格做分割，否则即使有空格也连在一起
echo 'this is a test' | awk '{print NF, $NF, $(NF-1)}'

```



