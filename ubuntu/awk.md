http://www.gnu.org/software/gawk/manual/gawk.html

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
```



