

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

curl -s https://testerhome.com/ | grep href | grep -o 'http[^\"]*'
```



