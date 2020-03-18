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

### 安装
- 无需root权限
- 源码安装
http://www.postgres.cn/docs/11/install-short.html
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

#### New DB user

- In linux:

```she
adduser user1
```

- postgres sql:

```sql
CREATE USER user1 WITH PASSWORD 'password';
CREATE DATABASE db1 OWNER user1;
GRANT ALL PRIVILEGES ON DATABASE db1 to user1;
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
```

```sql
select * from pg_hba_file_rules;
```

- set path

```
hba_file (string)
```



### 反斜杠命令

#### show databases: 
```
psql -l
\l
SELECT datname FROM pg_database;
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



### 一些命令

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

### Knowledge points

#### Default value

```sql
CREATE TABLE products (product_no integer, name text, price numeric DEFAULT 9.99);
CREATE TABLE products (product_no integer DEFAULT nextval('products_product_no_seq'), ...);
CREATE TABLE products (product_no SERIAL, ...);
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
t1 CROSS JOIN t2 -- equals to t1,t2, equals to JOIN, equals to INNER JOIN
on t1.xx = t2.xx -- two xx column
using(xx)        -- one xx column
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
EXPLAIN (format JSON/XML/YAML) SELECT ....

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

- MVCC - Multi Version Concurrency Control，MVCC中，对查询（读）数据的锁请求与写数据的锁请求不冲突。

- Default Isolation level: Read Uncommitted = Read Committed
- SET TRANSACTION ... ...

| Isolation level  | Dirty Read                 | Nonrepeatable Read | Phantom Read               | Serialization Anormaly |
| ---------------- | -------------------------- | ------------------ | -------------------------- | ---------------------- |
| Read uncommitted | **Allowed, but not in PG** | Possible           | Possible                   | Possible               |
| Read committed   | Not possible               | Possible           | Possible                   | Possible               |
| Repeatable read  | Not possible               | Not possible       | **Allowed, but not in PG** | Possible               |
| Serializable     | Not possible               | Not possible       | Not possible               | Not possible           |

- locks: http://www.postgres.cn/docs/11/explicit-locking.html

- check locks: 

  ```sql
   select * from pg_locks;
   SELECT * FROM pg_locks pl LEFT JOIN pg_stat_activity psa ON pl.pid = psa.pid;
   SELECT * FROM pg_locks pl LEFT JOIN pg_prepared_xacts ppx
      ON pl.virtualtransaction = '-1/' || ppx.transaction;
      select pg_blocking_pids(<pid>);
  ```

  

  