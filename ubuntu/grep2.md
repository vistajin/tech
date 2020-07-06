**G**lobal search **R**egular **E**xpression and **P**rint out the line

```sh
grep pattern file
# ignore case
grep -i pattern file
# show NOT match instead
grep -v pattern file
# only show match wording/content
grep -o pattern file
# use regular expression
grep -E pattern file
# grep 'a[0-9]\{10\}'   == grep -E 'a[0-9]{10}'
# recurve
grep -r pattern dir/
# show the first match only
grep -m1 pattern file
# show line number
grep -n pattern file

curl -s https://testerhome.com/ | grep href | grep -o 'http[^\"]*' | while read line; do curl -s -I $line | grep "200 OK" && echo $line || echo ERR $line; done
```

egrep：支持扩展正则表达式，相当于grep -E

fgrep：不支持正则表达式，只能匹配写死的字符串，但是速度奇快，效率高，fastgrep

