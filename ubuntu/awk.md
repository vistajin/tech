http://www.gnu.org/software/gawk/manual/gawk.html

```sh
# 开始和结束
awk 'BEGIN{}END{}'

echo -e "A line 1\nA line 2" | awk 'BEGIN{print "Start"} {print} END{print "end"}'


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


ll | awk '{print $9}'

echo "1-2-3-4" | awk -F- '{print $3}'
```



