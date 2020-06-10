```sh

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
