

#### Stat location

stats_temp_directory = 'pg_stat_tmp'

copy to pg_stat after shotdown

```sql
-- check table insert/delete/update counts etc...
select *, now() from pg_stat_all_tables where relname = 'xx';
analyze xx; -- to show back the n_live_tup
```

postgresql-12.2/src/backend/postmaster/pgstat.c

pgstat_read_statsfiles(Oid onlydb, bool permanent, bool deep)

pgstat_write_statsfiles(bool permanent, bool allDbs)

#### Track activities

```sql
# check running query
select query, query_start from pg_stat_activity;
# close not work for 12???
set track_activities = off;
```

```properties
track_activities = on # 收集SQL执行开始时间以及SQL语句的内容
track_counts = on # 收集数据库活动信息（如表新增的行数，删除的行数等）， autovaceem进程需要用到
track_io_timing = off
track_functions = none                 # none, pl, all
track_activity_query_size = 1024       # (change requires restart) SQl语句可以显示的长度
stats_temp_directory = 'pg_stat_tmp'
```

#### log_statement_stats

```sql
show log_statement_stats;
set log_statement_stats=on;
set client_min_messages = debug;
postgres=# select * from jly;
LOG:  QUERY STATISTICS
DETAIL:  ! system usage stats:
!	0.000181 s user, 0.000060 s system, 0.000240 s elapsed
!	[0.020447 s user, 0.006815 s system total]
!	11412 kB max resident size
!	0/0 [4216/0] filesystem blocks in/out
!	0/0 [15/667] page faults/reclaims, 0 [0] swaps
!	0 [0] signals rcvd, 0/0 [0/0] messages rcvd/sent
!	0/0 [79/1] voluntary/involuntary context switches
```

#### pg_stat_statements

```sql
create extension pg_stat_statements;
```

- postgresql.conf

```properties
shared_preload_libraries = 'pg_stat_statements'
# add below
pg_stat_statements.max = 1000
pg_stat_statements.track = all
```

```sql
\d pg_stat_statements 

select pg_stat_statements_reset();
select * from pg_stat_statements order by total_time desc limit 1 offset 0;
-- 调用次数
select * from pg_stat_statements order by calls desc limit 1 offset 0;
-- 单次sql执行时间
select * from pg_stat_statements order by total_time / calls desc limit 1 offset 0;
-- 按shared buffer “未命中块读”倒序输出
select * from pg_stat_statements order by shared_blks_read desc limit 1 offset 0;

select row_number() over() as rn, * from (select query, ' calls: ' || calls || ' total_time_ms:' || round(total_time::numeric, 2) ||' avg_time_ms:'||round((total_time::numeric/calls),2) as stats from pg_stat_statements order by total_time desc limit 20) t;
```

#### pg_stat_bgwriter

```sql
\x
select * from pg_stat_bgwriter;
```



### sar



### Nagios

https://github.com/digoal/blog/blob/d7336aeb9fc9cc82714189f16d67d22e47f9d369/201306/20130603_01.md

https://github.com/digoal/blog/blob/d7336aeb9fc9cc82714189f16d67d22e47f9d369/201306/20130603_02.md



#### log_statement

```sql
alter role vista set log_statement = 'all';
```

#### hstore

```sql
create extension hstore;
create table test (id int primary key, info text, crt_time timestamp(0));

create table table_change_rec (
    id serial8 primary key,
    relid oid,
    table_schema text,
    table_name text,
    when_tg text,
    level text,
    op text,
    old_rec hstore,
    new_rec hstore,
    crt_time timestamp without time zone default now(),
    username text,
    client_addr inet,
    client_port int
);
-- 23:40 TODO
```

