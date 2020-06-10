```sh

# replace line with row in all lines
sed 's/line/row/g' test.txt

# only replace the 2nd match in each line
sed 's/i/QQQQ/2' test.txt

# only show those changed lines
sed -n 's/number 2/qqqqq/p' test.txt

# delete all lines starts from 2nd line
sed '2,$d' test.txt

# delete all lines
sed 'd' test.txt

# delete 3rd line
sed '3d' test.txt

# delete 1-3 line
sed '1,3d' test.txt
sed '/1/,/3/d' test.txt

```
