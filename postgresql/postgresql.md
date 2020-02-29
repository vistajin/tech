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
SELECT * FROM T1; -- This will also select T2
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
