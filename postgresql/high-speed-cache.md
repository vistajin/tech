## 本地高速缓存 

### pgfincore

- git: https://git.postgresql.org/gitweb/?p=pgfincore.git;a=summary
- github: https://github.com/klando/pgfincore
- man posix_fadvise
- https://git.postgresql.org/gitweb/?p=pgfincore.git;a=summary

#### install

```shell
git clone git://git.postgresql.org/git/pgfincore.git

export PATH=/usr/local/pgsql/bin:$PATH
make clean
make
su
export PATH=/usr/local/pgsql/bin:$PATH
make install

# show functions of pgfincore
nm -A /usr/local/pgsql/lib/pgfincore.so
```

```sql
test=# create extension pgfincore;
CREATE EXTENSION
--- show installed functions of pgfincore
\df pgf*
```

#### test

```sql
-- change shared buffer in postgresql.conf
shared_buffers = 32M

show shared_buffers;

create table user_info (id int primary key, info text, crt_time timestamp);
insert into user_info select generate_series(1, 5000000), md5(random()::text), clock_timestamp();

select pg_total_relation_size('user_info')/1024/1024||'MB';
 ?column? 
----------
 472MB
(1 row)

```

```shell
echo 3 > /proc/sys/vm/drop_caches

vi test.sql
\set id random(1,5000000) #\setrandom id 1 5000000 setrandom not work, command not found
select * from user_info where id = :id;

## test without cache
pgbench -M prepared -n -r -f ./test.sql -c 16 -j 4 -T 10 test
query mode: prepared
number of clients: 16
number of threads: 4
duration: 10 s
number of transactions actually processed: 718734
latency average = 0.223 ms
tps = 71853.505482 (including connections establishing)
tps = 71872.357404 (excluding connections establishing)
statement latencies in milliseconds:
         0.000  \set id random(1,5000000)
         0.220  select * from user_info where id = :id;
```

```sql
-- toast table for info field
select relname from pg_class where oid = (select reltoastrelid from pg_class where relname = 'user_info');
-- enable cache
select * from pgfadvise_willneed('user_info'::regclass);
select * from pgfadvise_willneed('user_info_pkey'::regclass);
select * from pgfadvise_willneed('pg_toast.pg_toast_16402'::regclass);
```

```shell
# test with cache
pgbench -M prepared -n -r -f ./test.sql -c 16 -j 4 -T 10 test
transaction type: ./test.sql
scaling factor: 1
query mode: prepared
number of clients: 16
number of threads: 4
duration: 10 s
number of transactions actually processed: 976121
latency average = 0.164 ms
tps = 97581.305497 (including connections establishing)
tps = 97605.710450 (excluding connections establishing)
statement latencies in milliseconds:
         0.000  \set id random(1,5000000)
         0.161  select * from user_info where id = :id;
```

```sql
-- disable again
select * from pgfadvise_dontneed('user_info'::regclass);
select * from pgfadvise_dontneed('user_info_pkey'::regclass);
select * from pgfadvise_dontneed('pg_toast.pg_toast_16402'::regclass);
```

## 异地高速缓存

### pgmemcache

pgmemcache is a set of PostgreSQL user-defined functions that provide an interface to memcached.

https://github.com/ohmu/pgmemcache

#### install

​	Dependency: pgmencache --> libmencached + postgresql ->libevent + memcached -> libevent

##### install libevent 

refer to pgbouncer.md

##### install memcached

- high-performance memory object caching system

- Package: https://memcached.org/downloads

- https://memcached.org/files/memcached-1.6.3.tar.gz

- install on both server and client (client no need start)

  ```shell
  # install libsasl2-dev
  sudo apt install libsasl2-dev
  
  tar -zxvf memcached-1.6.3.tar.gz
  cd memcached-1.6.3/
  ./configure --help
  # 64bit pointer_size = 64 needs more space, no < 20 billion key, can use 32bit
  ./configure --prefix=/opt/memcached-1.6.3 --enable-sasl --enable-64bit
  make
  su
  make install
  exit
  cd /opt/memcached-1.6.3/share/man/man1
  man ./memcached.1
  # memcached - high-performance memory object caching system
  
  # start with shared memory 800M (client no need)
  cd /opt/memcached-1.6.3/bin/
  ./memcached -d -u postgres -m 800
  
  # check process running
  ps -ewf | grep memcached
  postgres  4381  2645  0 19:12 ?        00:00:00 ./memcached -d -u postgres -m 800
  postgres  4531  7460  0 19:12 pts/1    00:00:00 grep --color=auto memcached
  
  # check port
  netstat -anp | grep 11211
  (Not all processes could be identified, non-owned process info
   will not be shown, you would have to be root to see it all.)
  tcp        0      0 0.0.0.0:11211           0.0.0.0:*               LISTEN      4381/./memcached    
  tcp6       0      0 :::11211                :::*                    LISTEN      4381/./memcached
  
  # check shared memory
  ipcs
  
  ------ Message Queues --------
  key        msqid      owner      perms      used-bytes   messages    
  
  ------ Shared Memory Segments --------
  key        shmid      owner      perms      bytes      nattch     status      
  0x00000000 491520     vistajin   600        67108864   2          dest         
  0x00000000 720897     vistajin   600        4194304    2          dest         
  0x00000000 753666     vistajin   600        524288     2          dest         
  0x00000000 2260995    vistajin   700        209160     2          dest         
  0x00000000 917509     vistajin   600        524288     2          dest         
  0x00000000 1212422    vistajin   600        524288     2          dest         
  0x00000000 1703943    root       600        393216     2          dest         
  0x00000000 1343496    vistajin   600        524288     2          dest         
  0x00000000 1376265    vistajin   600        524288     2          dest         
  0x00000000 1474570    vistajin   600        524288     2          dest         
  0x00000000 1572875    vistajin   600        524288     2          dest         
  0x00000000 2031628    vistajin   700        30000      2          dest         
  0x0052e2c1 1769485    postgres   600        56         6                       
  0x00000000 1867790    vistajin   600        524288     2          dest         
  0x00000000 1900559    vistajin   600        16777216   2          dest         
  0x00000000 1998864    vistajin   600        524288     2          dest         
  
  ------ Semaphore Arrays --------
  key        semid      owner      perms      nsems     
  0x00000000 65536      www-data   600        1         
  
  ```

##### install libmencached

- https://libmemcached.org/libMemcached.html

- https://launchpad.net/libmemcached/+download

- https://launchpad.net/libmemcached/1.0/1.0.18/+download/libmemcached-1.0.18.tar.gz

- install

  ```shell
  cd
  wget https://launchpad.net/libmemcached/1.0/1.0.18/+download/libmemcached-1.0.18.tar.gz
  tar -zxvf libmemcached-1.0.18.tar.gz
  cd libmemcached-1.0.18/
  ## apply hotfix, see in below session
  ./configure --prefix=/opt/libmemcached-1.0.18 --with-memcached=/opt/memcached-1.6.3/bin/memcached
  make
  su
  make install
  echo "/opt/libmemcached-1.0.18/lib" >> /etc/ld.so.conf
  exit
  ldconfig -p | grep libmemcached
  ############ weird, nothing return, install failed??????
  ls -al /usr/lib | grep libmem
  #### also nothing return
  ```

  ```c++
  /* HOTFIX */
  /*
  clients/memflush.cc:42:22: error: ISO C++ forbids comparison between pointer and integer [-fpermissive]
     if (opt_servers == false)
                        ^~~~~
  clients/memflush.cc:51:24: error: ISO C++ forbids comparison between pointer and integer [-fpermissive]
       if (opt_servers == false)
                          ^~~~~
  */
  diff -up ./clients/memflush.cc.old ./clients/memflush.cc
  --- ./clients/memflush.cc.old	2017-02-12 10:12:59.615209225 +0100
  +++ ./clients/memflush.cc	2017-02-12 10:13:39.998382783 +0100
  @@ -39,7 +39,7 @@ int main(int argc, char *argv[])
   {
     options_parse(argc, argv);
   
  -  if (opt_servers == false)
  +  if (!opt_servers)
     {
       char *temp;
   
  @@ -48,7 +48,7 @@ int main(int argc, char *argv[])
         opt_servers= strdup(temp);
       }
   
  -    if (opt_servers == false)
  +    if (!opt_servers)
       {
         std::cerr << "No Servers provided" << std::endl;
         exit(EXIT_FAILURE);
  diff -up ./clients/memaslap.c.old ./clients/memaslap.c
  --- ./clients/memaslap.c.old	2020-02-04 14:11:45.029205068 +0100
  +++ ./clients/memaslap.c	2020-02-04 14:12:05.409115227 +0100
  @@ -32,6 +32,15 @@
   #include "ms_setting.h"
   #include "ms_thread.h"
   
  +/* global structure */
  +ms_global_t ms_global;
  +
  +/* global stats information structure */
  +ms_stats_t ms_stats;
  +
  +/* global statistic structure */
  +ms_statistic_t ms_statistic;
  +
   #define PROGRAM_NAME    "memslap"
   #define PROGRAM_DESCRIPTION \
                           "Generates workload against memcached servers."
  diff -up ./clients/ms_memslap.h.old ./clients/ms_memslap.h
  --- ./clients/ms_memslap.h.old	2020-02-04 14:11:50.072182835 +0100
  +++ ./clients/ms_memslap.h	2020-02-04 14:12:13.268080586 +0100
  @@ -117,13 +117,13 @@ typedef struct global
   } ms_global_t;
   
   /* global structure */
  -ms_global_t ms_global;
  +extern ms_global_t ms_global;
   
   /* global stats information structure */
  -ms_stats_t ms_stats;
  +extern ms_stats_t ms_stats;
   
   /* global statistic structure */
  -ms_statistic_t ms_statistic;
  +extern ms_statistic_t ms_statistic;
   
   #ifdef __cplusplus
   }
  ```

  ##### install pgmemcache

  ```shell
  git clone https://github.com/ohmu/pgmemcache
  cd pgmemcache
  cp -R /opt/libmemcached-1.0.18/include/libmemcached-1.0 ./libmemcached
  cp -R /opt/libmemcached-1.0.18/include/libmemcached-1.0 ./libmemcached-1.0
  cp -R /opt/libmemcached-1.0.18/include/libhashkit-1.0 libhashkit-1.0
  
  vi Makefile
  SHLIB_LINK = -L/opt/libmemcached-1.0.18/lib -lmemcached -lsasl2
  
  su
  export PATH=$PATH:/usr/local/pgsql/bin
  make
  
  make install
  /bin/mkdir -p '/usr/local/pgsql/lib'
  /bin/mkdir -p '/usr/local/pgsql/share/extension'
  /bin/mkdir -p '/usr/local/pgsql/share/extension'
  /usr/bin/install -c -m 755  pgmemcache.so '/usr/local/pgsql/lib/pgmemcache.so'
  /usr/bin/install -c -m 644 .//pgmemcache.control '/usr/local/pgsql/share/extension/'
  /usr/bin/install -c -m 644 .//ext/pgmemcache--unpackaged--2.0.sql .//ext/pgmemcache--2.0--2.1.sql .//ext/pgmemcache--2.1--2.1.1.sql .//ext/pgmemcache--2.1.1--2.1.2.sql .//ext/pgmemcache--2.1.2--2.2.0.sql .//ext/pgmemcache--2.2.0--2.3.0.sql pgmemcache--2.3.0.sql pgmemcache.control '/usr/local/pgsql/share/extension/'
  
  ### check
  ll /usr/local/pgsql/lib/pgmemcache.so 
  -rwxr-xr-x 1 root root 39120 Mar 29 22:45 /usr/local/pgsql/lib/pgmemcache.so*
  ```

#### config

edit postgresql.conf

```properties
shared_preload_libraries = 'pgmemcache' # (change requires restart)
pgmemcache.default_servers = '127.0.0.1:11211' # multiple memcached separated bt comma ,
pgmemcache.default_behavior = 'BINARY_PROTOCOL:1' # multiple setting separated  by comma ,
```

```shell
# verify can access
telnet localhost 11211
quit

# restart postgres
pg_ctl restart -m fast
psql
```

#### Test

```sql
CREATE EXTENSION pgmemcache;

postgres=# \df 
                                              List of functions
 Schema |        Name         | Result data type |                 Argument data types                 | Type 
--------+---------------------+------------------+-----------------------------------------------------+------
 public | memcache_add        | boolean          | key text, val text                                  | func
 public | memcache_add        | boolean          | key text, val text, expire interval                 | func
 public | memcache_add        | boolean          | key text, val text, expire timestamp with time zone | func
 public | memcache_append     | boolean          | key text, val text                                  | func
 public | memcache_append     | boolean          | key text, val text, expire interval                 | func
 public | memcache_append     | boolean          | key text, val text, expire timestamp with time zone | func
 public | memcache_decr       | bigint           | key text                                            | func
 public | memcache_decr       | bigint           | key text, decrement bigint                          | func
 public | memcache_delete     | boolean          | key text                                            | func
 public | memcache_delete     | boolean          | key text, hold interval                             | func
 public | memcache_flush_all  | boolean          |                                                     | func
 public | memcache_get        | text             | key bytea                                           | func
 public | memcache_get        | text             | key text                                            | func
 public | memcache_get_multi  | SETOF record     | keys bytea[], OUT key text, OUT value text          | func
 public | memcache_get_multi  | SETOF record     | keys text[], OUT key text, OUT value text           | func
 public | memcache_incr       | bigint           | key text                                            | func
 public | memcache_incr       | bigint           | key text, increment bigint                          | func
 public | memcache_prepend    | boolean          | key text, val text                                  | func
 public | memcache_prepend    | boolean          | key text, val text, expire interval                 | func
 public | memcache_prepend    | boolean          | key text, val text, expire timestamp with time zone | func
 public | memcache_replace    | boolean          | key text, val text                                  | func
 public | memcache_replace    | boolean          | key text, val text, expire interval                 | func
 public | memcache_replace    | boolean          | key text, val text, expire timestamp with time zone | func
 public | memcache_server_add | boolean          | server_hostname text                                | func
 public | memcache_set        | boolean          | key bytea, val text                                 | func
 public | memcache_set        | boolean          | key text, val bytea                                 | func
 public | memcache_set        | boolean          | key text, val text                                  | func
 public | memcache_set        | boolean          | key text, val text, expire interval                 | func
 public | memcache_set        | boolean          | key text, val text, expire timestamp with time zone | func
 public | memcache_stats      | text             |                                                     | func
(30 rows)

postgres=# select memcache_set('name', 'vista');
 memcache_set 
--------------
 t
(1 row)

postgres=# select memcache_get('name');
 memcache_get 
--------------
 vista
(1 row)
```



```sql
create table memcache_test(userid int8, pwd text);
insert into memcache_test select generate_series(1, 1000000), md5(clock_timestamp()::text);

create or replace function memcache_test_upd() returns trigger as $$
begin
    if old.pwd != new.pwd then
        perform memcache_set('memcache_test_' || new.userid || '_pwd', new.pwd);
    end if;
    return null;
end;
$$ language 'plpgsql' strict;
create trigger memcache_test_upd after update on memcache_test for each row execute procedure memcache_test_upd();

create or replace function memcache_test_ins() returns trigger as $$
begin
    perform memcache_set('memcache_test_' || new.userid || '_pwd', new.pwd);
    return null;
end;
$$ language 'plpgsql' strict;
create trigger memcache_test_ins after insert on memcache_test for each row execute procedure memcache_test_ins();

create or replace function memcache_test_del() returns trigger as $$
begin
    perform memcache_delete('memcache_test_' || new.userid || '_pwd');
    return null;
end;
$$ language 'plpgsql' strict;
create trigger memcache_test_del after delete on memcache_test for each row execute procedure memcache_test_del();

create or replace function auth (i_userid int8, i_pwd text) returns boolean as $$
declare
v_input_pwd_md5 text;
v_user_pwd_md5 text;
begin
    v_input_pwd_md5 := i_pwd;
    select memcache_get('memcache_test_' || i_userid || '_pwd') into v_user_pwd_md5;
    if (v_user_pwd_md5 <> '') then
        raise notice 'hit in memcache.';
        raise notice 'v_user_pwd_md5: %', v_user_pwd_md5;
        raise notice 'i_pwd: %', i_pwd;
        if (v_input_pwd_md5 = v_user_pwd_md5) then
            return true;
        else
            return false;
         end if;
     else
         select pwd into v_user_pwd_md5 from memcache_test where userid = i_userid;
         if found then
             raise notice 'hit in table.';
             if (v_input_pwd_md5 = v_user_pwd_md5) then
                 return true;
             else
                 return false;               
             end if;
         else
             return false;
        end if;
    end if;
exception
when others then
    return false;
end;
$$ language plpgsql strict;
```







#### summary usage after install

```shell
cd /opt/memcached-1.6.3/bin/
./memcached -d -u postgres -m 800
psql
postgres=# select memcache_stats();
      memcache_stats       
---------------------------
 Server: 127.0.0.1 (11211)+
 pid: 21498               +
 uptime: 89               +
 time: 1585572785         +
 version: 1.6.3           +
 pointer_size: 64         +
 rusage_user: 0.16274     +
 rusage_system: 0.11624   +
 curr_items: 1            +
 total_items: 2           +
 bytes: 69                +
 curr_connections: 3      +
 total_connections: 4     +
 connection_structures: 4 +
 cmd_get: 3               +
 cmd_set: 2               +
 get_hits: 2              +
 get_misses: 1            +
 evictions: 0             +
 bytes_read: 175          +
 bytes_written: 151       +
 limit_maxbytes: 838860800+
 threads: 4               +
                          +
 
(1 row)
```