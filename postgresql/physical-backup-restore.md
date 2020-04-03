![](/home/vistajin/tech/postgresql/物理还原.png)

### 物理冷备份

- $PGDATA

### 物理热备份

- 适合小版本范围
- 不能跨平台
- $PGDATA
- All real path of pg_tblspc under $PGDATA

#### 备份步骤

##### 配置更改

- postgresql.conf

  ```properties
  wal_level = replica
  archive_mode = on               # enables archiving; off, on, or always
                                                         # (change requires restart)
  archive_command = 'DATE=`date +%Y%m%d`; DIR=/home/postgres/archive/$DATE; (test -d $DIR || mkdir -p $DIR) & cp %p $DIR/%f'
  ```

  %p - $PGDATA/pg_wal/xxxxx, v12之前是pg_xlog

  %f  - xxxxx 

##### 检查配置是否生效

```sql
psql
\c test
checkpoint;
select pg_switch_wal();
```

```shell
ll /home/postgres/archive/20200401/
total 49160
drwx------ 2 postgres postgres     4096 Apr  1 21:28 ./
drwx------ 3 postgres postgres     4096 Apr  1 21:25 ../
-rw------- 1 postgres postgres 16777216 Apr  1 21:25 000000010000000000000034
-rw------- 1 postgres postgres 16777216 Apr  1 21:28 000000010000000000000035
-rw------- 1 postgres postgres 16777216 Apr  1 21:28 000000010000000000000036
```

##### 执行备份

- after archive setup successfully, go ahead for backup, case use pg_basebackup or mannually copy files:

###### pg_basebackup

- 流复制协议备份，本地必须使用tar模式，异地无所谓，如果要同目录结构的话使用p模式
- create replication role or can use super user directly

- ```sql
create role rep nosuperuser replication login connection limit 32 encrypted password 'abcabc123123';
  
  postgres=# \du rep
               List of roles
   Role name |   Attributes   | Member of 
  -----------+----------------+-----------
   rep       | Replication   +| {}
             | 32 connections | 
  ```
  
- pg_hba.conf

  ```
  host replication rep 0.0.0.0/0 md5
  pg_ctl reload
  ```

  

- start backup

  ```shell
  # backup
  mkdir /home/postgres/pgbak
  cd /home/postgres/pgbak
  pg_basebackup -F t -X none -D ./ -h 127.0.0.1 -p 5432 -U rep
  
  # backup result
  ll
  total 55372
  drwxrwxr-x  2 postgres postgres     4096 Apr  1 21:51 ./
  drwxr-xr-x 15 postgres postgres     4096 Apr  1 21:47 ../
  -rw-------  1 postgres postgres     1536 Apr  1 21:51 16461.tar
  -rw-------  1 postgres postgres 39906304 Apr  1 21:51 base.tar
  -rw-------  1 postgres postgres 16778752 Apr  1 21:51 pg_wal.tar
  
  # 16461 tar is the table space
  /usr/local/pgsql/data/pg_tblspc$ ll
  total 8
  drwx------  2 postgres postgres 4096 Mar 31 23:03 ./
  drwx------ 19 postgres root     4096 Apr  1 21:42 ../
  lrwxrwxrwx  1 postgres postgres   18 Mar 31 23:03 16461 -> /home/postgres/tmp/
  
  # check base content
  tar -tvf base.tar | less
  
  # check archive (WAL) after run backup command
  ll /home/postgres/archive/20200401/
  total 81932
  drwx------ 2 postgres postgres     4096 Apr  1 21:51 ./
  drwx------ 3 postgres postgres     4096 Apr  1 21:25 ../
  -rw------- 1 postgres postgres 16777216 Apr  1 21:25 000000010000000000000034
  -rw------- 1 postgres postgres 16777216 Apr  1 21:28 000000010000000000000035
  -rw------- 1 postgres postgres 16777216 Apr  1 21:28 000000010000000000000036
  -rw------- 1 postgres postgres 16777216 Apr  1 21:51 000000010000000000000037
  -rw------- 1 postgres postgres 16777216 Apr  1 21:51 000000010000000000000038
  -rw------- 1 postgres postgres      340 Apr  1 21:51 000000010000000000000038.00000028.backup
  ```

  -D, --pgdata=DIRECTORY receive base backup into directory

  -F, --format=p|t       output format (plain (default), tar)

  -X, --wal-method=none|fetch|stream   include required WAL files with specified method, 如果none则没有pg_wal.tar

###### backup manually

- run start backup

  ```sql
  select pg_start_backup(now()::text);
  ```

- backup label created in $PGDATA

  ```shell
  ll $PGDATA
  total 152
  drwx------ 19 postgres root      4096 Apr  1 22:05 ./
  drwxr-xr-x  7 root     root      4096 Mar 28 16:18 ../
  -rw-------  1 postgres postgres   237 Apr  1 22:05 backup_label
  
  # check the content of the label
  cat /usr/local/pgsql/data/backup_label 
  START WAL LOCATION: 0/3A000028 (file 00000001000000000000003A)
  CHECKPOINT LOCATION: 0/3A000060
  BACKUP METHOD: pg_start_backup
  BACKUP FROM: master
  START TIME: 2020-04-01 22:05:39 CST
  LABEL: 2020-04-01 22:05:39.072143+08
  START TIMELINE: 1
  ```

- check if backup in progress

  ```sql
  select pg_is_in_backup();
  ```

- now can start to copy below folders to another directly

  - $PGDATA
  - $PGDATA/pg_tblspc
  - archive folder e.g. /home/postgres/archive

- after above folders copied, stop backup by sql command

  ```sql
  select pg_stop_backup();
  ```

### 还原
#### 还原点

#### recovery_target_name

```sql
postgres=# select pg_create_restore_point('20200403001');
2020-04-03 21:43:36.090 CST [23393] LOG:  restore point "20200403001" created at 0/42000140
2020-04-03 21:43:36.090 CST [23393] STATEMENT:  select pg_create_restore_point('20200403001');
 pg_create_restore_point 
-------------------------
 0/42000140
(1 row)
```



#### recovery_target_time

```sql
postgres=# select now();
              now              
-------------------------------
 2020-04-03 21:46:58.635402+08
(1 row)
```



#### recovery_target_xid

```sql
postgres=# select txid_current();
 txid_current 
--------------
          518
(1 row)
```





#### 还原步骤

##### 添加数据库操作

- before restore, do some update to database to see if can restore to this point

```sql
create table t_restore_test (id int);
insert into t_restore_test values(123321);

checkpoint;
select pg_switch_wal();
```

##### stop postgres

```shell
pg_ctl stop -m fast
```

##### delete table space folder and $PGDATA

```shell
rm -rf $PGDATA/*
rm -rf /home/postgres/tmp/*
```

##### copy backuped tar and unzip

```shell
cd $PGDATA
cp /home/postgres/pgbak/base.tar .
cp /home/postgres/pgbak/16461.tar /home/postgres/tmp/
tar -xvf base.tar
rm -rf base.tar
cd /home/postgres/tmp/
tar -xvf 16461.tar
rm -rf 16461.tar 
```

##### edit postgresql.conf (no more recovery.conf in v12)

```properties
# today is 20200403, i backup the db on 20200402, so i only need to copy today's WAL
# which contains my changes for t_restore_test
restore_command = 'cp /home/postgres/archive/20200403/%f %p'
```

##### touch recovery.signal in $PGDATA

##### start up postgres

```shell
pg_ctl start
```

##### check if the changes today also recovered

```sql
postgres=# select * from t_restore_test;
   id   
--------
 123321
(1 row)
```



