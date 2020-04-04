

### pg_dump

- -F c 备份为二进制格式，压缩存储并且可被pg_restore用于精细还原
- -F p 备份为文本，大库不推荐

```shell
# backup
postgres@vistajin-pc:~/test$ pg_dump -F c -f ./test.dump -C -E UTF8 -h 127.0.0.1 -p 5432 -U postgres test

# check backup file
postgres@vistajin-pc:~/test$ ll
total 2156
drwxrwxr-x  2 postgres postgres    4096 Apr  3 22:04 ./
drwxr-xr-x 17 postgres postgres    4096 Apr  3 21:59 ../
-rw-rw-r--  1 postgres postgres 2195177 Apr  3 22:04 test.dump

# drop
drop database test;

# restore
# create db to connect to restore (there is no create database in the dump file)
create database test;
pg_restore -d test ./test.dump

# export TOC
# https://github.com/digoal/blog/blob/master/201204/20120412_01.md
# ./src/bin/pg_dump/pg_backup_archiver.c
pg_restore -f ./test.toc -F c -l ./test.dmp 
# restore with modified TOC
pg_restore -F c -L ./test.toc -d test -h 127.0.0.1 -U postgres
```



### pg_dumpall

- 全局元数据包括用户密码，数据库，表空间
- 仅支持文本格式

### COPY

- 用于SQL子集或表的备份还原

```sql
postgres=# copy (select * from t_restore_test) to stdout;
123321

copy (select * from t_restore_test) to '/home/postgres/test/t_restore_test.bak';
```

