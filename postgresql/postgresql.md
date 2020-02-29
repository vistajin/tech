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

### createdb / dropdb / psql

#### show databases: 
```
\l
```
#### change current database: 
```
\c db_name
```
#### show tables: 
```
\dt
```
#### load data from file: 
```sql
COPY table_name FROM '/path/to/some/file.txt'
```

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
