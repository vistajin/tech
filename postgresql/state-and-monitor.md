

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

