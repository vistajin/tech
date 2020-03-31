### 冷备份

- $PGDATA

### 热备份

- $PGDATA

- All real path of pg_tblspc under $PGDATA

- archive_mode = on

  ```properties
  archive_mode = on               # enables archiving; off, on, or always
                                                         # (change requires restart)
  archive_command = 'DATE=`date +%Y%m%d`; DIR=/home/postgres/archive/$DATE; (test -d $DIR || mkdir -p $DIR) & cp %p $DIR/%f'
  ```

  

- 