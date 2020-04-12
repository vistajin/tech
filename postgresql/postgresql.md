### Postgresql History
- 1973 University INGRES (IBM system R)
- 1982 INGRES
- 1985 Post-Ingres
- 1988 POSTGRES version 1 - 1993 version 4 (END)
- 1995 Postgres95 (Andrew Yu, Jolly Chen)
- 1996 Postgress (first open source)

### 特性
- 没有回滚段，旧的数据直接记录在数据文件中，回滚很快
- 进程模式
- 只支持堆表（oracle），不支持索引组织表（oracle，mysql），全表扫面快

### Overview

- Cluster (initdb)
  - Database(s) (CREATE DATABASE) 
    - Schema(s) (CREATE SCHEMA) 
      - Table(s)
        - Row(s)
        - Column(s)
      - View(s)
      - Index(s)
      - Function(s)
      - Sequence(s)
      - Other(s)

### Physical Structure

Table          <-------->Datafile(s)
Index          <-------->Datafile(s)
Toast          <-------->Datafile(s)
Sequence <-------->Datafile(s)
​                                       Controlfile
            Archived<----WALs

Note: Datafile default size = 1GB (./configuration --help:  --with-segsize=SEGSIZE)

### Process Structure

![](/home/vistajin/tech/postgresql/postgresql-proc-structure.png)

source code: src/backend/postmaster

- postmaster - 所有数据库进程的主进程（负责坚挺和fork子进程）
- startup - 主要用于数据库恢复的进程
- syslogger - 记录系统日志
- pgstat - 收集统计信息
- pgarch - 如果开启了归档，那么postmaster会fork一个归档进程
- checkpointer - 负责检查点的进程
- bgwriter - 负责把shared buffer中的脏数据写入磁盘的进程
- autovacuum launcher -- 负责回收垃圾数据的进程，如果开启了autovacuum的话，那么postmaster会fork这个进程
- autovacuum worker - 负责回收垃圾数据的worker进程，是launcher进程fork出来的。

### Physical Structure 物理结构

- Where is the physical file of an object?

  ```sql
  create tablespace my_space location '/var/lib/postgresql/tablespace';
  create table tt1 (key int) tablespace my_space;
  select * from pg_relation_filepath('tt1');
              pg_relation_filepath             
  ---------------------------------------------
   pg_tblspc/16957/PG_12_201909212/16384/16958
  (1 row)
  ```

  <$PGDATA>/pg_tblspc/<tablespace_oid>/<PG_Version>/<db_oid>/<filenode_oid>

  ```bash
  lrwxrwxrwx 1 postgres postgres 30 Mar 24 13:19 16957 -> /var/lib/postgresql/tablespace
  postgres@0830b402c800:/$ ls -l $PGDATA/pg_tblspc/16957
  lrwxrwxrwx 1 postgres postgres 30 Mar 24 13:19 /var/lib/postgresql/data/pg_tblspc/16957 -> /var/lib/postgresql/tablespace
  postgres@0830b402c800:/$ ls -l /var/lib/postgresql/tablespace
  total 4
  drwx------ 3 postgres postgres 4096 Mar 24 13:19 PG_12_201909212
  postgres@0830b402c800:/$ ls -l /var/lib/postgresql/tablespace/PG_12_201909212/16384/16958 
  -rw------- 1 postgres postgres 0 Mar 24 13:19 /var/lib/postgresql/tablespace/PG_12_201909212/16384/16958
  ```

- One Page (8K)

  ^^^^^^^^^^^^^^^^^^^^^^

  PageHeaderData (24Bytes)

  ^^^^^^^^^^^^^^^^^^^^^^

  ItemIdData (Array of (offset, length)) pairs pointing to the actual items, 4 bytes per item)

  ^^^^^^^^^^^^^^^^^^^^^^

  Fres Space (The unallocated space. New item pointers are allocated from the start of this area, new items from the end)

  ^^^^^^^^^^^^^^^^^^^^^^

  Items (The actual items themselves)

  ^^^^^^^^^^^^^^^^^^^^^^

  Special Space (Index access method specific data. Different methods store different data. Empty in ordinary tables. Ab access method shoud always initialize its pages with PageInit and then set its own opaque fields)

  ^^^^^^^^^^^^^^^^^^^^^^

  

### 安装

- 无需root权限

- 源码安装
  http://www.postgres.cn/docs/11/install-short.html

  

  https://ftp.postgresql.org/pub/source/v12.2/postgresql-12.2.tar.bz2

  ```shell
  sudo apt-get install libreadline6 libreadline6-dev
  sudo apt-get install zlib1g-dev
  
  ./configure
  make
  su
  make install
  adduser postgres
  mkdir /usr/local/pgsql/data
  chown postgres /usr/local/pgsql/data
  su - postgres
  /usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
  /usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data >logfile 2>&1 &
  /usr/local/pgsql/bin/createdb test
  /usr/local/pgsql/bin/psql test
  ln -s /usr/local/pgsql/bin/psql /usr/bin/
  vi ~/.bashrc
  export PGDATA=/usr/local/pgsql/data
  source .bashrc
  # check port
netstat -anp | grep postgres
  ```

  
  
- 下载deb安装
  https://www.postgresql.org/download/linux/ubuntu/

- docker
https://hub.docker.com/_/postgres
```sh
sudo docker run --name postgres -e POSTGRES_PASSWORD=abc123 -d postgres
sudo docker exec -it 0830b402c800 /bin/bash
su postgres
psql
SELECT version();
```

### New DB user

- In linux:

```she
adduser user1
```

- postgres sql:

```sql
CREATE USER user1 WITH PASSWORD 'password';
CREATE DATABASE db1 OWNER user1;
GRANT ALL PRIVILEGES ON DATABASE db1 to user1;
alter user vista superuser ;
ctrl+d
psql -U user1 -d db1 -h 127.0.0.1 -p 5432
-- or
user1@0830b402c919:/$ psql -d db1 -h 127.0.0.1 -p 5432
```



### Client Authentication

- pg_hba.conf (host based authentication)

```properties
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     trust
# IPv4 local connections:
host    all             all             127.0.0.1/32            trust
# IPv6 local connections:
host    all             all             ::1/128                 trust

# TYPE
# local - 本地unix socket
# host, hostssl, hostnossl - ssl表示网络传输的数据使用加密方式传输

# METHOD
# trust - NO need password
# reject - deny connect
# md5 - 检验过程密码加密传输，但是其他数据是否加密传输要看配置的认证类型是否为SSL
# password - 检验过程密码明文传输，如果认证类型为SSL，则同样会被加密
```

```sql
select * from pg_hba_file_rules;
```

- set path

```
hba_file (string)
```



### 反斜杠命令

#### Show Help for command

```sql
\h create tablespace
```



#### show databases: 

```sql
psql -l
\l
\l+
SELECT datname FROM pg_database;
select  pg_database.datname, pg_database_size(pg_database.datname) AS size from pg_database;
```
#### change current database: 
```
\c db_name
```
#### show tables: 
```
\dt
```
#### describe table

```sql
\d table_name
```

#### show timing

```sql
\timing
```

#### show role/user

```sql
\du
create role role_name;
drop role role_name;
SELECT rolname FROM pg_roles;
createuser name
dropuser name
```

#### show tablespace

```sql
\db
```

#### switch display mode (column to row) 切换显示模式（行<->列）

```
\x
```

#### List function filter by keyword

```sql
\df *.*read_file*
                                    List of functions
   Schema   |       Name       | Result data type |      Argument data types      | Type 
------------+------------------+------------------+-------------------------------+------
 pg_catalog | pg_read_file     | text             | text                          | func
 pg_catalog | pg_read_file     | text             | text, bigint, bigint          | func
 pg_catalog | pg_read_file     | text             | text, bigint, bigint, boolean | func
 pg_catalog | pg_read_file_old | text             | text, bigint, bigint          | func
```

#### Verbose 

```
\set VERBOSITY verbose
```



### 一些命令

#### Restart

```
pg_ctl restart -m fast
```



#### load data from file: 

```sql
COPY table_name FROM '/path/to/some/file.txt'
```

#### create/drop db

```sql
psql / createdb / dropdb
CREATE DATABASE db_name; -- createdb db_name
CREATE DATABASE dbname OWNER rolename; -- createdb -O rolename dbname
CREATE DATABASE dbname TEMPLATE template0; -- createdb -T template0 dbname
-- 模板数据库
select * from pg_database where datistemplate is true;
```



#### Tablespace 表空间

```sql
CREATE TABLESPACE fastspace LOCATION '/ssd1/postgresql/data';
SET default_tablespace = space1;
select * from pg_tablespace;
```

`pg_global`表空间被用于共享系统目录。pg_default 默认表空间



#### Create Table

```sql
create table t2(like t1);
CREATE TABLE test1 (
    a text COLLATE "de_DE",
    b text COLLATE "es_ES",
);
-- COLLATE 类似语言编码，不同COLLATE排序不同。数据库，索引等都可指定COLLATE

ALTER TABLE some_table OWNER TO <some_one>;
```



#### initdb

```sql
initdb --locale=sv_SE
initdb --locale=fr_BE.UTF-8
initdb --locale=fr_CA --lc-monetary=en_US
```

```
1.创建pg的data主目录，以及其所有子目录 
2.生成配置文件postgresql.conf 
3.创建template1数据库 
4.对template1数据库加载初始化数据 
5.复制template1到template0数据库 
6.复制template1到postgres数据库
```

#### vacuum

垃圾收集并根据需要分析一个数据库。适度运行标准`VACUUM`运行比少量运行`VACUUM FULL`要更好。`TRUNCATE`会立刻移除该表的整个内容，而不需要一次后续的`VACUUM`或`VACUUM FULL`来回收现在未被使用的磁盘空间。

```plsql
vacuum verbose analyze t1;
vacuum full t1;
vacuum full verbose;
```

#### autovacuum

- `autovacuum_naptime` (`integer`): postgresql.conf or command line, default 60s
- `autovacuum_max_workers` (`integer`): set when start up, default 3
- `log_autovacuum_min_duration` (`integer`)： postgresql.conf or command line, default -1 means no log, if N then log all clean action that longer than N ms

#### 重建索引

- reindex

  ```sql
  reindex index xxx
  reindex table xxx
  ```
- alter index / drop index
  ```sql
  CREATE INDEX CONCURRENTLY
  ```

#### Install Extension 安装插件

```sql
create extension pageinspect;
select * from fsm_page_contents(get_raw_page('t2', 'main', 0));

create table hot_test (id int primary key, info text);
insert into hot_test values(1, 'vista');
-- below can functions are from pageinspect
select * from page_header(get_raw_page('hot_test', 0));
    lsn    | checksum | flags | lower | upper | special | pagesize | version | prune_xid 
-----------+----------+-------+-------+-------+---------+----------+---------+-----------
 0/92528C8 |        0 |     0 |    28 |  8152 |    8192 |     8192 |       4 |         0
(1 row)

select * from heap_page_items(get_raw_page('hot_test', 0));
 lp | lp_off | lp_flags | lp_len | t_xmin | t_xmax | t_field3 | t_ctid | t_infomask2 | t_infomask | t_hoff | t_bits | t_oid |         t_data         
----+--------+----------+--------+--------+--------+----------+--------+-------------+------------+--------+--------+-------+---------------
---------
  1 |   8152 |        1 |     34 |    700 |      0 |        0 | (0,1)  |           2 |       2050 |     24 |        |       | \x010000000d76
69737461
(1 row)

select * from page_header(get_raw_page('hot_test_pkey', 0));
    lsn    | checksum | flags | lower | upper | special | pagesize | version | prune_xid 
-----------+----------+-------+-------+-------+---------+----------+---------+-----------
 0/9252928 |        0 |     0 |    64 |  8176 |    8176 |     8192 |       4 |         0
(1 row)

select * from heap_page_items(get_raw_page('hot_test_pkey', 0));
 lp | lp_off | lp_flags | lp_len | t_xmin | t_xmax | t_field3 | t_ctid | t_infomask2 | t_infomask | t_hoff | t_bits | t_oid | t_data 
----+--------+----------+--------+--------+--------+----------+--------+-------------+------------+--------+--------+-------+--------
  1 |  12642 |        2 |      2 |        |        |          |        |             |            |        |        |       | 
  2 |      4 |        0 |      0 |        |        |          |        |             |            |        |        |       | 
  3 |      1 |        0 |      0 |        |        |          |        |             |            |        |        |       | 
  4 |      0 |        0 |      0 |        |        |          |        |             |            |        |        |       | 
  5 |      1 |        0 |      0 |        |        |          |        |             |            |        |        |       | 
  6 |      0 |        0 |      0 |        |        |          |        |             |            |        |        |       | 
  7 |      0 |        0 |      0 |        |        |          |        |             |            |        |        |       | 
  8 |      0 |        0 |      0 |        |        |          |        |             |            |        |        |       | 
  9 |      0 |        0 |      0 |        |        |          |        |             |            |        |        |       | 
 10 |      0 |        0 |  24568 |        |        |          |        |             |            |        |        |       | 
(10 rows)

update hot_test set info = 'VistaJIN' where id = 1;
-- run above pageinspect sql to see the differences
vacuum hot_test;

mydb=# select * from heap_page_items(get_raw_page('hot_test', 0));
 lp | lp_off | lp_flags | lp_len | t_xmin | t_xmax | t_field3 | t_ctid | t_infomask2 | t_infomask | t_hoff | t_bits | t_oid |            t_
data            
----+--------+----------+--------+--------+--------+----------+--------+-------------+------------+--------+--------+-------+--------------
----------------
  1 |   8152 |        1 |     34 |    700 |    701 |        0 | (0,2)  |       16386 |        258 |     24 |        |       | \x010000000d7
669737461
  2 |   8112 |        1 |     37 |    701 |      0 |        0 | (0,2)  |       32770 |      10242 |     24 |        |       | \x01000000135
6697374614a494e
(2 rows)

mydb=# vacuum hot_test ;
VACUUM
mydb=# select * from heap_page_items(get_raw_page('hot_test', 0));
 lp | lp_off | lp_flags | lp_len | t_xmin | t_xmax | t_field3 | t_ctid | t_infomask2 | t_infomask | t_hoff | t_bits | t_oid |            t_
data            
----+--------+----------+--------+--------+--------+----------+--------+-------------+------------+--------+--------+-------+--------------
----------------
  1 |      2 |        2 |      0 |        |        |          |        |             |            |        |        |       | 
  2 |   8152 |        1 |     37 |    701 |      0 |        0 | (0,2)  |       32770 |      10498 |     24 |        |       | \x01000000135
6697374614a494e
(2 rows)

```

#### Comment table

```sql
comment on table table_name is 'xxx xxx xx';
\dt+
```



### Knowledge points

#### Materialized Views 物化视图 （since 9.3）

```sql
CREATE MATERIALIZED VIEW mymatview AS SELECT * FROM mytab WITH NO DATA;
CREATE UNIQUE INDEX rental_category ON mymatview (category);
-- 全量刷新，更快但阻塞select
REFRESH MATERIALIZED VIEW mymatview;
-- 增量刷新，更慢但不阻塞select，since 9.4
REFRESH MATERIALIZED VIEW CONCURRENTLY rental_by_category;
```

https://www.postgresql.org/docs/9.3/rules-materializedviews.html

#### 类型转换 type convert/cast

```sql
select E'abc\\';
select cast('1 hour' as interval);
select '1 hour'::interval;
select interval '1 hour';
```

#### 隐藏字段

```sql
---1.oid 
oid是object identifier的简写,其相关的参数设置default_with_oids设置一般默认是false,或者创建表时指定with (oids=false)，其值长度32bit,实际的数据库系统应用中并不能完全保证其唯一性; 
---2.tableoid 
是表对象的一个唯一标识符，可以和pg_class中的oid联合起来查看 
---3.xmin 
是插入的事务标识符,是用来标识不同事务下的一个版本控制。每一次更新该行都会改变这个值。可以和mvcc版本结合起来看 
---4.xmax 
是删除更新的事务标识符，如果该值不为0，则说明该行数据当前还未提交或回滚。比如设置begin事务时可以明显看到该值的变化 
---5.cmin 
插入事务的命令标识符,从0开始 
---6.cmax 
删除事务的命令标识符，或者为0 
---7.ctid 
是每行数据在表中的一个物理位置标识符，和oracle的rowid类似，但有一点不同，当表被vacuum full或该行值被update时该值可能会改变。所以定义表值的唯一性最好还是自己创建一个序列值的主键列来标识比较合适。不过使用该值去查询时速度还是非常快的。
-- 相同事务ID
insert into test select generate_series(1,3),repeat('kenyon',2);
```

#### Function state 函数三态

- Immutable: if output is the same when input parameters are the same, can declare it as immutable

  ```sql
  alter function nextval(regclass)  immutable;
  ```

- Stable: stable at where clause, mutable in select

  ```sql
  alter function nextval(regclass) stable;
  ```

- Volatile

  ```sql
  alter function nextval(regclass) stable;
  ```


- Check

  ```sql
  select  proname,proargtypes,provolatile from pg_proc where ...
  ```

  

#### Dollar Quoting

```sql
SELECT $$hello's the name of the game$$;
SELECT E'hello\'s the name of the game';
SELECT $vista$hello's the name of the $$ game$vista$;
```

#### Prepare statement

```sql
mydb=# prepare ps(int) as select * from t1 where num = $1;
PREPARE
mydb=# execute ps(1);
 num |  name  
-----+--------
   1 | aaaaaa
(1 row)
```

#### Transaction 事务操作

```sql
BEGIN;
COMMIT;
ROLLBACK;
SAVEPOINT a;
ROLLBACK to a;
-- 即使执行过程中出错仍然可以继续后续语句，只是自动rollback 出错的语句。
\set ON_ERROR_ROLLBACK on
```



#### Default value

```sql
CREATE TABLE products (product_no integer, name text, price numeric DEFAULT 9.99);
CREATE TABLE products (product_no integer DEFAULT nextval('products_product_no_seq'), ...);
CREATE TABLE products (product_no SERIAL, ...);

CREATE TABLE described(a int);
COMMENT ON TABLE described IS $$I'm describing this,
including newlines and an apostrophe in the contraction "I'm."$$;

CREATE TABLE json(data json);
INSERT INTO json(data) VALUES ($${"quotation": "'there is no time like the present'"}$$);
```

#### Constrains
```sql
CREATE TABLE products (product_no integer, name text, price numeric CHECK (price > 0));
CREATE TABLE products (product_no integer, name text, price numeric CONSTRAINT positive_price CHECK (price > 0));
CREATE TABLE products (product_no integer, name text, 
    price numeric CHECK (price > 0), 
    discounted_price numeric CHECK (discounted_price > 0), 
    CHECK (price > discounted_price));
CREATE TABLE products (product_no integer, name text,
    price numeric CHECK (price > 0),
    discounted_price numeric,
    CHECK (discounted_price > 0 AND price > discounted_price)
)

CREATE TABLE products (product_no integer UNIQUE, ...);
CREATE TABLE products (product_no integer, ..., UNIQUE(product_no));

CREATE TABLE orders (..., product_no integer REFERENCES products (product_no), ...);
CREATE TABLE t1 (..., FOREIGN KEY (b, c) REFERENCES other_table (c1, c2));
...REFERENCES orders ON DELETE CASCADE/RESTRICT...

------------------------------------------------Index exclude using---------------------------------------------------------------
CREATE EXTENSION btree_gist;
CREATE TABLE test (
    user_id INTEGER, startend TSTZRANGE, EXCLUDE USING gist (user_id WITH =,startend WITH &&)
);
mydb=# insert into test values (1, '[2020-03-01 14:30+08:00, 2020-03-01 15:30:+08:00)');
INSERT 0 1
mydb=# insert into test values (1, '[2020-04-01 14:30+08:00, 2020-04-01 15:30:+08:00)');
INSERT 0 1
mydb=# insert into test values (1, '[2020-03-01 15:00+08:00, 2020-03-01 16:00:+08:00)');
ERROR:  conflicting key value violates exclusion constraint "test_user_id_startend_excl"
DETAIL:  Key (user_id, startend)=(1, ["2020-03-01 07:00:00+00","2020-03-01 08:00:00+00")) conflicts with existing key (user_id, startend)=(1, ["2020-03-01 06:30:00+00","2020-03-01 07:30:00+00")).
```

#### Change column type
```sql
ALTER TABLE products ALTER COLUMN price TYPE numeric(10,2);
```

#### Change table name
```sql
ALTER TABLE products RENAME TO items;
```

#### Grant permission
```sql
GRANT UPDATE ON table_name TO user_name;
GRANT ALL ON table_name TO user_name;
REVOKE ALL ON table_name FROM PUBLIC;

with grant option -- 
```

#### Row security policy
http://www.postgres.cn/docs/11/ddl-rowsecurity.html

#### Transaction
```sql
BEGIN;
COMMIT;
SAVEPOINT the_point;
ROLLBACK TO the_point;
-- 一个事物最大2^32条SQL（因为cmin，cmax的长度是4bytes）
-- 事务可以执行DDL，DML，DCL
-- 事务不能执行：
create tablespace
create database
-- 事务不能使用concurrently并行创建索引
```
#### Window function
```sql
SELECT depname, empno, salary, avg(salary) OVER (PARTITION BY depname) FROM empsalary;
SELECT depname, empno, salary, rank() OVER (PARTITION BY depname ORDER BY salary DESC) FROM empsalary;
SELECT salary, sum(salary) OVER () FROM empsalary;
SELECT salary, sum(salary) OVER (partition by depname) FROM empsalary;
SELECT salary, sum(salary) OVER (ORDER BY salary) FROM empsalary;
SELECT sum(salary) OVER w, avg(salary) OVER w
  FROM empsalary
  WINDOW w AS (PARTITION BY depname ORDER BY salary DESC);
```

#### Inherits
```sql
CREATE TABLE T2 (...) INHERITS (T1);
SELECT * FROM T1; -- This will also select T2, equals to: SELECT * FROM T1*;
SELECT * FROM ONLY T1; -- UPDATE, DELETE also support ONLY
-- all constraint on parent table must also in child table, child table can have more constrains like filed1 > xxx
-- also inherits index, unique key, primary key, table space
create table c2(like c1 including all) inherits (c1);
alter table c2 no inherit c1;
alter table c2 drop constraint c1_c2_check;
-- can't inherit c1 now, need to add back the constraint to inherit again
alter table c2 add constraint c1_c2_check (xx > 0);
alter table c2 inherit c1;
-- query parent table will also query child table and grandson table by default
-- to select only current table, add only
select * from ONLY  table_xx;
-- insert, copy only on current table, others will also apply to child

show constraint_exclusion ;
 constraint_exclusion 
----------------------
 partition
 
```
#### Function
```sql
CREATE FUNCTION concat_lower_or_upper(a text, b text, uppercase boolean DEFAULT false)
RETURNS text
AS
$$
 SELECT CASE
        WHEN $3 THEN UPPER($1 || ' ' || $2)
        ELSE LOWER($1 || ' ' || $2)
        END;
$$
LANGUAGE SQL IMMUTABLE STRICT;

SELECT concat_lower_or_upper('Hello', 'World', true);
SELECT concat_lower_or_upper('Hello', 'World');
SELECT concat_lower_or_upper(a => 'Hello', b => 'World');
SELECT concat_lower_or_upper(a => 'Hello', uppercase => true, b => 'World');
SELECT concat_lower_or_upper(a => 'Hello', uppercase => true, b => 'World');
SELECT concat_lower_or_upper('Hello', 'World', uppercase => true);
```

#### Schema
```sql
CREATE SCHEMA myschema;
DROP SCHEMA myschema CASCADE; -- all objects like tables, views will be dropped too
CREATE SCHEMA schema_name AUTHORIZATION user_name;
-- 以pg_开头的模式名被保留用于系统目的，所以不能被用户所创建。
-- default SCHEMA is "public"
SHOW search_path;
SET search_path TO myschema,public;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
-- 第一个“public”是方案，第二个“public”指的是“每一个用户”。第一种是一个标识符，第二种是一个关键词
-- pg_catalog
ALTER ROLE user SET search_path = "$user"; -- remove public schema for user
```

#### Partition 表分区
```sql
CREATE TABLE measurement (
    city_id         int not null,
    logdate         date not null,
    peaktemp        int,
    unitsales       int
) PARTITION BY RANGE (logdate);  -- 按照记录日期分区

CREATE TABLE measurement_y2007m11 PARTITION OF measurement
    FOR VALUES FROM ('2007-11-01') TO ('2007-12-01');
    
CREATE TABLE measurement_y2006m02 PARTITION OF measurement
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01')
    PARTITION BY RANGE (peaktemp); -- 创建子分区
    
CREATE TABLE measurement_y2008m01 (
    CHECK ( logdate >= DATE '2008-01-01' AND logdate < DATE '2008-02-01' )
) INHERITS (measurement);  -- 使用继承
ALTER TABLE measurement_y2006m02 NO INHERIT measurement; -- 保留独立表数据

DROP TABLE measurement_y2006m02;  -- 删除数据（快速）， need ACCESS EXCLUSIVE lock

ALTER TABLE measurement DETACH PARTITION measurement_y2006m02;  -- even better option to remove old data

SET enable_partition_pruning = on;
```

#### Return value from insert/update/delete
```sql
INSERT INTO users (firstname, lastname) VALUES ('Joe', 'Cool') RETURNING id;
UPDATE products SET price = price * 1.10
  WHERE price <= 99.99
  RETURNING name, price AS new_price;
DELETE FROM products WHERE obsoletion_date = 'today' RETURNING *;
```

#### Join table
```sql
cross join -- 笛卡尔
t1,t2, equals to JOIN, equals to INNER JOIN
on t1.xx = t2.xx -- two xx column
using(xx)        -- one xx column,  equals to NATURAL JOIN
```

#### GROUPING SETS,CUBE, ROLLUP
```sql
SELECT brand, size, sum(sales) FROM items_sold GROUP BY GROUPING SETS ((brand), (size), ());
-- 计算和值for不同的brand,size组合，（）表示所有值都可以，即计算总数

SELECT brand, size, sum(sales) FROM items_sold GROUP BY ROLLUP ((brand), (size));
SELECT brand, size, sum(sales) FROM items_sold GROUP BY CUBE ((brand), (size));
-- http://www.postgres.cn/docs/11/queries-table-expressions.html
```

#### Combine Query
```sql
UNION [ALL]
INTERSECT [ALL]
EXCEPT [ALL]
```

#### distinct on

```sql
create table a6(id integer, name varchar(10));
insert into a6 values(1, ' 001');
insert into a6 values(1, '002');
insert into a6 values(2, '003');
insert into a6 values(2, '004');
select distinct on (id) id, name from a6;
id | name
---+--------
1 | 001
2 | 003
(2 rows)
---- 如果加上order by的话，可以选出每个distinct字段内的最大最小值，相当于group by了
---- 可以distinct on多个列
```



#### With Clause

```sql
WITH RECURSIVE -- 允许在查询中查找自己，也就是递归

WITH RECURSIVE pseudo-entity-name(column-names) AS (
    Initial-SELECT
UNION ALL
    Recursive-SELECT using pseudo-entity-name
)
Outer-SELECT using pseudo-entity-name

-- 例子1：
WITH RECURSIVE t(n) AS (  -- n是列名
    VALUES (1)            -- t表刚开始只有一个值1
  UNION ALL
    SELECT n+1 FROM t WHERE n < 100 -- 第一次执行到这里n=1, 小于100，满足条件于是有了新的值n+1=2
                                    -- 如果没有RECURSIVE，这t表在这里是不能被引用到
                                    -- 接着继续select直到n=100，最终t表的值为1,2,3,...,100
)
SELECT sum(n) FROM t;

-- 例子2：
WITH RECURSIVE factorial(F,n) AS ( -- 表factorial，列名：F，n
    SELECT 1 F, 3 n                -- 初始表值：1，3
UNION ALL
    SELECT F*n F, n-1 n from factorial where n>1 -- n=3，大于1，表新值：3，2
                                                 -- n=2，大于1，表新值：6，1
)
SELECT F from factorial where n=1;               -- F=6
```

#### Date time funcitons
```sql
select  date '2001-09-28' + integer '7';
select date '2001-09-28' + interval '1 hour';
--https://www.postgresql.org/docs/9.1/functions-datetime.html
```

#### Enum type
```sql
CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy'); 
-- case sensitive
-- can't compare with other enum, need convert to test if need ::text
-- sort order is the sequence in definition, i.e. sad < ok < happy
-- can add new value but can't remove, can change enum name, can't change order.
```

#### lateral
```sql
SELECT * FROM foo, LATERAL (SELECT * FROM bar WHERE bar.id = foo.bar_id) ss;
-- 在LATERAL(这里可以关联(引用)lateral左边的表或子句)  
```
#### 特殊数据类型
- serial, bigserial, smallserial
- money (lc_monetary)
- bytea
- boolean
- point,line,lseg,box,path,polygon,circle
- cidr,inet,macaddr,macaddr8
- bit
- tsvector,tsquery 文本搜索
- UUID
- XML
- JSON,JSONB
- ARRAY
- Combination -- CREATE TYPE xxx AS
- range：int4range,int8range,numrange,tsrange,tstzrange,daterange
- domain: CREATE DOMAIN posint AS integer CHECK (VALUE > 0);
- OID: WITH OIDS, default_with_oids
- pg_lsn: 日志序列号
- 伪类型: any, anyelement, anyenum, anyrange,cstring, ....

#### 特殊运算符

包含运算符：@>, 被包含：<@，重叠：&&

完全在左边：<<，完全在右边：>>，邻接：-|-，

匹配：@@ or @@@，后面紧跟：<->

```sql
select ARRAY[1,4,3] @> ARRAY[3,1,3];  -- t
select ARRAY[1,4,3] @> ARRAY[3,1,6];  -- f
-- https://www.postgresql.org/docs/current/functions-range.html
to_tsvector('fat cats ate rats') @@ to_tsquery('cat & rat') -- true
to_tsquery('fat') <-> to_tsquery('rat') -- 'fat' <-> 'rat'
-- http://www.postgres.cn/docs/11/functions-textsearch.html
```

#### Index
- 索引相关的配置

  ```
  enable_bitmapscan = on
  enable_hashagg = on
  enable_hashjoin = on
  enable_indexscan = on
  enable_material = on
  enable_mergejoin = on
  enable_nestloop = on
  enable_seqscan = on
  enable_sort = on
  enable_tidscan = on
  ```

  ```sql
  create table test (c1 int, c2 int);
  insert into test selcect 1, generate_series(1, 10000);
  create index idx_text_1 on test(c1, c2);
  set enable_seqscan = off;
  -- Now it can use idx_text_1 for below sql
  select * from test where c2 = 100;
  ```

- B-tree: default. 只有B-tree能够被声明为唯一, PostgreSQL会自动为定义了一个唯一约束或主键的表创建一个唯一索引
```sql
CREATE INDEX test2_info_nulls_low ON test2 (info NULLS FIRST);
CREATE UNIQUE INDEX name ON table (column [, ...]);
CREATE UNIQUE INDEX idx_t1_ab ON t1 USING btree (a, b) INCLUDE (c);
```
- Hash: 只能处理简单等值比较
```sql
CREATE INDEX name ON table USING HASH (column);
```
- GiST
- SP-GiST
- GIN
- BRIN

#### 表达式索引
```sql
CREATE INDEX test1_lower_col1_idx ON test1 (lower(col1));
CREATE INDEX people_names ON people ((first_name || ' ' || last_name));
```
####  部分索引
```sql
CREATE INDEX orders_unbilled_index ON orders (order_nr)
    WHERE billed is not true;
CREATE UNIQUE INDEX tests_success_constraint ON tests (subject, target)
    WHERE success;
```

#### Index Only Scan - 覆盖索引 Converting index
如果select的字段都包含在index中，postgres将会进行索引扫描而不回表。Index-Only 扫描不支持表达式。
```sql
explain (analyze,verbose,timing,costs,buffers) select id,c1,c2,c3,info,crt_time from t1 where id=1;
create index idx_t1_1 on t1 (id) include(c1,c2,c3,info,crt_time);
-- other columns stored in index leaf page，无需到堆取数据
create index idx_t2_1 on t2 (id,c1,c2,c3,info,crt_time);
-- index size big, insert much slower than include
```

####  analyze

```sql
-- check analyze history
select * from pg_stat_user_tables;
-- run analyze
analyze [VERBOSE] [TABLE_NAME] [COLUMN_NAME];
-- analyze就起到一个更新统计信息的作用, 使PostgreSQL采用更加合理的查询。
-- 例如update或者insert某个表后，不执行analyze，那么explain看到的结果不会发生变化
EXPLAIN ANALYZE SELECT/UPDATE/DELETE
explain (analyze true,buffers true) select * from ...
```

#### Explain

```sql
EXPLAIN [option] statement
option:
ANALYZE  -- 执行statement，得到真实的运行时间以及统计信息
VERBOSE -- 输出详细信息
COSTS       -- 输出cost值，默认打开
BUFFERS  -- 输出本次query shared 或 local buffer的信息，包括命中，未命中，脏写
TIMING      -- 输出时间开销
FORMAT {TEXT|XML|JSON|YAML}  -- 输出格式

explain (verbose,analyze,costs,buffers,timing) select * from cities ;

SELECT relpages, reltuples FROM pg_class WHERE relname = '<table_name>';
mydb=# SELECT relpages, reltuples FROM pg_class WHERE relname = 't1';
 relpages | reltuples 
----------+-----------
        1 |         4
-- 开销 = relpages + 0.01 * reltuples = 1.04
mydb=# EXPLAIN SELECT * FROM t1;
                    QUERY PLAN                    
--------------------------------------------------
 Seq Scan on t1  (cost=0.00..1.04 rows=4 width=9)
(1 row)

```

- Cost calculation related table & view

  pg_stats

  ```sql
  select * from pg_stats where tablename = 'xxx' and attname = 'field1';
  ```

  pg_class: relpages, reltuples

- Parameters

  seq_page_cost: 全表扫描的单个数据块的代价因子

  random_page_cost: 索引扫描的单个数据块的代价因子

  cpu_tuple_cost: 处理每条记录的CPU开销代价因子

  cpu_index_tuple_cost: 索引扫描时每个索引条目的CPU开销代价因子

  cpu_operator_cost: 操作符或函数的开销代价因子

```sql
select * from pg_proc where proname = 'int4lt'; -- procost = 1
```

- auto_explain plug-in: monitor sql which execution time is long

  ```shell
  vi $PGDATA/postgresql.conf
  shared_preload_libraries='pg_stat_statements,auto_explain'
  auto_explain.log_min_duration=100ms
  pg_ctl restart -m fast
  ```

  

#### Full-text search, 全文检索

- default config in postgresql.conf

  ```properties
  default_text_search_config = 'pg_catalog.english'
  ```

- List of text search configurations

  ```
  \dF
  ```

#### pg_trgm 近似匹配



#### Trigger

```sql
CREATE OR REPLACE FUNCTION abort()
    RETURNS event_trigger
  LANGUAGE plpgsql
    AS $$
BEGIN
    if current_user = 'postgres' then
        RAISE EXCEPTION 'event: %, command: %', tg_event, tg_tag;
    end if;
END;
$$;

create event trigger a on ddl_command_start when TAG IN ('CREATE TABLE', 'DROP TABLE') execute procdeure abort();
select * from pg_event_trigger;
```

#### 视图攻击

```sql
-- https://github.com/digoal/blog/blob/d7336aeb9fc9cc82714189f16d67d22e47f9d369/201307/20130710_01.md
create or replace function attack(int,int,text,int,text,text,text) returns boolean as $$  
declare  
begin  
  raise notice '%,%,%,%,%,%,%', $1,$2,$3,$4,$5,$6,$7;  
  return true;  
end;
$$ language plpgsql cost 0.00000000000000000000001;  

select * from view where attack(xxx,xxx,xxx);

--  to avoid attack
create view xxx with(security_barrier) as select * from x where xx=xx;  
```



### 数据库管理

#### pgBader - The PostgreSQL log analyzer

https://pgbadger.darold.net/

#### pg_ctl

```plsql
pg_ctl status
pg_ctl initdb -D /var/lib/postgresql/data2
/usr/lib/postgresql/12/bin/pg_ctl -D /var/lib/postgresql/data2 -l logfile start
pg_ctl -o "-F -p 5433" restart
```

#### different replication solutions

https://www.postgresql.org/docs/12/different-replication-solutions.html

- Shared Disk Failover: NAS, no sync as only one db copy

- File System (Block Device) Replication

- Write-Ahead Log (WAL) Shipping: built-in streaming replication

  - write WAL  = XLOG

  - WAL的中心概念是数据文件（存储着表和索引）的修改在写入磁盘之前，必须先记入日志记录

  - wal contain a history of all changes made to the database.

  - max_wal_size: default 1GB

  - similar to Oracle REDO log

  - fsync, default on, 更新数据写入磁盘时系统必须等待WAL的写入完成. if off, 提高了性能，无法保证在系统崩溃时最近的事务能够得到恢复

  - synchronous_commit：默认值是ON，表明必须等待WAL完成后才返回事务状态信息。OFF对于数据的一致性不存在风险，能够为系统的性能带来不小的提升。SET LOCAL synchronous_commit TO OFF

  - http://postgres.cn/docs/11/runtime-config-wal.html

    ```sql
    alter system set wal_level= 'replica';
    alter system set archive_mode= 'on';
    alter system set archive_command = '/bin/cp -i %p /pgdata/10/archive_wal/%f';
    select pg_switch_wal();
    ```

  - Monitor what are writen to WAL (pg_waldump)

    ```sql
    select * from pg_ls_waldir() order by modification asc;
               name           |   size   |      modification      
    --------------------------+----------+------------------------
     000000010000000000000009 | 16777216 | 2020-03-14 12:50:25+00
     00000001000000000000000A | 16777216 | 2020-03-14 12:55:19+00
     000000010000000000000008 | 16777216 | 2020-03-14 12:58:59+00
    
    make some create table/insert/delete actions then run below command pg_waldump
    ```

    ```sql
    pg_waldump -f $PGDATA/pg_wal/000000010000000000000008
    ---------------------------------------------------------------
    rmgr: Heap        len (rec/tot):     54/    54, tx:        668, lsn: 0/08001140, prev 0/08001108, desc: DELETE off 4 flags 0x00 KEYS_UPDATED , blkref #0: rel 1663/16384/16917 blk 0
    rmgr: Transaction len (rec/tot):     34/    34, tx:        668, lsn: 0/08001178, prev 0/08001140, desc: COMMIT 2020-03-14 12:58:51.756115 UTC
    rmgr: Standby     len (rec/tot):     50/    50, tx:          0, lsn: 0/080011A0, prev 0/08001178, desc: RUNNING_XACTS nextXid 669 latestCompletedXid 668 oldestRunningXid 669
    rmgr: Standby     len (rec/tot):     50/    50, tx:          0, lsn: 0/080011D8, prev 0/080011A0, desc: RUNNING_XACTS nextXid 669 latestCompletedXid 668 oldestRunningXid 669
    rmgr: XLOG        len (rec/tot):    114/   114, tx:          0, lsn: 0/08001210, prev 0/080011D8, desc: CHECKPOINT_ONLINE redo 0/80011D8; tli 1; prev tli 1; fpw true; xid 0:669; oid 25109; multi 1; offset 0; oldest xid 480 in DB 13408; oldest multi 1 in DB 16384; oldest/newest commit timestamp xid: 0/0; oldest running xid 669; online
    rmgr: Standby     len (rec/tot):     50/    50, tx:          0, lsn: 0/08001288, prev 0/08001210, desc: RUNNING_XACTS nextXid 669 latestCompletedXid 668 oldestRunningXid 669
    ```

    lsn: Log Sequence Number

- Logical Replication

- Trigger-Based Master-Standby Replication

- Statement-Based Replication Middleware

- Asynchronous Multimaster Replication

- Synchronous Multimaster Replication

#### backup

1. SQL转储

   ##### pg_dump

   - dump based on template0
   - run ANALYZE after dump
   - no role and table space will be dump

   ```plsql
   pg_dump dbname > dumpfile
   psql dumpfile < dbname
   psql --set ON_ERROR_STOP=on dbname < infile
   -- transaction mode, rollback when any error
   psql -1 dbname < infile
   psql --single-transaction dbname < infile
   -- dump db from another server
   pg_dump -h host1 dbname | psql -h host2 dbname
   -- dump and zip, used for large size db
   pg_dump dbname | gzip > filename.gz
   gunzip -c filename.gz | psql dbname
   cat filename.gz | gunzip | psql dbname
   -- dump and split in files
   pg_dump dbname | split -b 1m - filename
   cat filename* | psql dbname
   -- dump to other format which is not psql format
   pg_dump -Fc dbname > filename
   pg_restore -d dbname filename
   -- dump in multiple threads
   pg_dump -j num -F d -f out.dir dbname
   pg_restore -j dbname filename
   ```

   #### pg_dumpall

   - will dump roles and table space

   ```sql
   pg_dumpall > dumpfile
   psql -f dumpfile postgres
   ```

   

2. 文件系统级别备份

   - must stop db

   ```shell
   tar -cf backup.tar /usr/local/pgsql/data
   ```

3. 连续归档和时间点恢复（PITR）

#### high availability

- patroni: 一个模板, 通过python来构建一个高可用的postgresql的解决方案, 使用的数据同步方式是postgresql的流复制方式

github: https://github.com/zalando/patroni

doc: https://patroni.readthedocs.io/en/latest/



### 配置 Configuration

#### postgresql.conf

- postgresql.conf path

```
/var/lib/postgresql/data/postgresql.conf
```
- reload postgresql.conf

```
pg_ctl reload
```

```sql
select pg_reload_conf();
```

- show current take effect config

```sql
select * from pg_file_settings;
```

- include other conf

```c
include 'filename'
include_if_exists 'filename'
include_dir 'directory'
```

- set path

```
config_file (string)
```



#### postgresql.auto.conf

- same path as postgresql.conf, don't edit manually, updated by ALTER SYSTEM
- load when postgresql.conf is loaded, override postgresql.conf

#### current session

```
set SESSION | LOCAL variable = | to value
select * from  pg_settings;
```

#### shell

```
postgres -c log_connections=yes -c log_destination='syslog'
env PGOPTIONS="-c geqo=off -c statement_timeout=5min" psql
```



#### show settings

```sql
show all;
select current_setting('application_name');
```



### 并发控制 Concurrency Control

#### 事务隔离

- MVCC - Multi Version Concurrency Control，MVCC中，对查询（读）数据的锁请求与写数据的锁请求不冲突。
- show transaction_isolation;
- Default Isolation level: Read Uncommitted = Read Committed
- SET TRANSACTION ... ...
- postgresql.conf: default_transaction_isolation = 'read committed'

| Isolation level  | Dirty Read                 | Nonrepeatable Read | Phantom Read               | Serialization Anormaly |
| ---------------- | -------------------------- | ------------------ | -------------------------- | ---------------------- |
| Read uncommitted | **Allowed, but not in PG** | Possible           | Possible                   | Possible               |
| Read committed   | Not possible               | Possible           | Possible                   | Possible               |
| Repeatable read  | Not possible               | Not possible       | **Allowed, but not in PG** | Possible               |
| Serializable     | Not possible               | Not possible       | Not possible               | Not possible           |

#### 锁 Lock

- locks: http://www.postgres.cn/docs/11/explicit-locking.html

- check locks: 

  ```sql
   select * from pg_locks;
   SELECT * FROM pg_locks pl LEFT JOIN pg_stat_activity psa ON pl.pid = psa.pid;
   SELECT * FROM pg_locks pl LEFT JOIN pg_prepared_xacts ppx
      ON pl.virtualtransaction = '-1/' || ppx.transaction;
      select pg_blocking_pids(<pid>);
    -- 查询存在锁的数据表
   select a.locktype,a.database,a.pid,a.mode,a.relation,b.relname -- ,sa.*
  from pg_locks a
  join pg_class b on a.relation = b.oid 
  inner join  pg_stat_activity sa on a.pid=sa.procpid;
  -- 查询某个表内,状态为lock的锁及关联的查询语句
  select a.locktype,a.database,a.pid,a.mode,a.relation,b.relname -- ,sa.*
  from pg_locks a
  join pg_class b on a.relation = b.oid 
  inner join  pg_stat_activity sa on a.pid=sa.procpid
  where a.database=382790774  and sa.waiting_reason='lock'
  order by sa.query_start;
  ```
  
- 表级锁
  
  ```sql
  LOCK table table_name;
  -- 查找锁住表的query， 例如 t1 被锁
  select oid, relname from pg_class where relname = 't1';
  select locktype,database,pid,relation ,mode from pg_locks where relation=<上一步的oid>;
  select usename,query,xact_start,pid from pg_stat_activity where pid=<上一步的pid>;
  -- mydb=# select usename,query,xact_start,pid from pg_stat_activity where pid=116;
  -- usename  |     query      |          xact_start          | pid 
  --      ----------+--------------+--------------------------+-----
  --   postgres | lock table t1; | 2020-03-19 13:45:37.75263+00 | 116
  -- (1 row)
  -- 强行终止
  select pg_terminate_backend(<上一步的pid>); 
  ```
  
  
  
- 行级锁

```sql
select * from table where f = 1 for update;
select * from table where f = 1 for update nowait; -- 55P03 if already locked by others
-- 连表查询加锁时，不支持单边连接形式，例如：
select u.*,r.* from db_user u left join db_role r on u.roleid=r.id for update;
-- 支持以下形式，并锁住了两个表中关联的数据：
select u.*,r.* from db_user u, db_role r where u.roleid=r.id for update;

```

- advisory lock

```sql
postgres=# \df *advisory*
                                       List of functions
   Schema   |               Name               | Result data type | Argument data types | Type 
------------+----------------------------------+------------------+---------------------+------
 pg_catalog | pg_advisory_lock                 | void             | bigint              | func
 pg_catalog | pg_advisory_lock                 | void             | integer, integer    | func
 pg_catalog | pg_advisory_lock_shared          | void             | bigint              | func
 pg_catalog | pg_advisory_lock_shared          | void             | integer, integer    | func
 pg_catalog | pg_advisory_unlock               | boolean          | bigint              | func
 pg_catalog | pg_advisory_unlock               | boolean          | integer, integer    | func
 pg_catalog | pg_advisory_unlock_all           | void             |                     | func
 pg_catalog | pg_advisory_unlock_shared        | boolean          | bigint              | func
 pg_catalog | pg_advisory_unlock_shared        | boolean          | integer, integer    | func
 pg_catalog | pg_advisory_xact_lock            | void             | bigint              | func
 pg_catalog | pg_advisory_xact_lock            | void             | integer, integer    | func
 pg_catalog | pg_advisory_xact_lock_shared     | void             | bigint              | func
 pg_catalog | pg_advisory_xact_lock_shared     | void             | integer, integer    | func
 pg_catalog | pg_try_advisory_lock             | boolean          | bigint              | func
 pg_catalog | pg_try_advisory_lock             | boolean          | integer, integer    | func
 pg_catalog | pg_try_advisory_lock_shared      | boolean          | bigint              | func
 pg_catalog | pg_try_advisory_lock_shared      | boolean          | integer, integer    | func
 pg_catalog | pg_try_advisory_xact_lock        | boolean          | bigint              | func
 pg_catalog | pg_try_advisory_xact_lock        | boolean          | integer, integer    | func
 pg_catalog | pg_try_advisory_xact_lock_shared | boolean          | bigint              | func
```

- skip locked

https://github.com/digoal/blog/blob/master/201610/20161018_01.md



### pgbench 轻量级的压力测试工具

```shell
# install pgbench
su -
cd src/bin/pgbench
make all
make install
ln -s /usr/local/pgsql/bin/pgbench /usr/bin
```



```shell
# 短连接
pgbench -M exteded -n -r -f ./xxx.sql -c 16 -j 4 -C -T 30
number of transactions actually processed: 57560
# 长连接
pgbench -M exteded -n -r -f ./xxx.sql -c 16 -j 4  -T 30
number of transactions actually processed: 3759633
# prepared
pgbench -M prepared -n -r -f ./xxx.sql -c 16 -j 4  -T 30
number of transactions actually processed: 3759633
# in another terminal
sar -w 1 100
```



