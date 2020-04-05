### dblink

#### install

```shell
cd /home/postgres/postgresql-12.2/contrib/dblink
make
su
make install
```

```sql
psql
create extension dblink;
\df *dblink*
```

#### document

https://www.postgresql.org/docs/12/dblink.html

Note: actually we don't use dblink now as the below postgres_fdw is better?



### postgres_fdw

#### install

```shell
cd /home/postgres/postgresql-12.2/contrib/postgres_fdw
make
su
make install
```

```sql
psql
create extension postgres_fdw;
\x
\df *fdw*
```

#### document

https://www.postgresql.org/docs/12/postgres-fdw.html

### Remote access using postgres_fdw

##### Create server on client PG

```sql
-- create server on pg5433
CREATE SERVER pg5432 FOREIGN DATA WRAPPER postgres_fdw OPTIONS (hostaddr '127.0.0.1', dbname 'test', port '5432');
```

##### Create user mapping on client PG

```sql
-- create mapping on pg5433
CREATE USER MAPPING FOR postgres SERVER pg5432 OPTIONS (user 'vista', password 'vista');
```

##### Create base table on server PG

```sql
create schema fdw;
set search_path to fdw,public;
create table fdw_test (id int primary key, info text, crt_time timestamp);
insert into fdw_test select generate_series (1, 1000), md5(random()::text), clock_timestamp();
```

#### Create foreign table on client PG

```sql
-- note: can't set primary constraint in foreign table
create foreign table ft_fdw_test (id int, info text, crt_time timestamp) server pg5432 options (schema_name 'fdw', table_name 'fdw_test');

-- check if can query the data which is on another server
select * from ft_fdw_test limit 10;
```



### materialized view

#### create materialized view

```sql
-- Create materialized view on the foreign table we created in previous step.
create materialized view mv_fdw_test as select * from ft_fdw_test with no data;
refresh materialized view mv_fdw_test with data;
create unique index idx_mv_fdw_test_id on mv_fdw_test (id);
refresh materialized view CONCURRENTLY mv_fdw_test with data;
```





