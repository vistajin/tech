### Background

As I don't have multiple hosts setup with postgres, I simulate the stream master-slave in the same host.

Master port 5432, slave port 5433



### Master

#### postgresql.conf

```properties
# replica = 9.6版本以前的archive和hot_standby --该级别支持wal归档和复制。
wal_level = replica
max_wal_senders = 10
wal_keep_segments = 256
synchronous_standby_names = '*'
# suggest
archive_mode = on
```

full version:

```properties
listen_addresses = '0.0.0.0'		# what IP address(es) to listen on;
max_connections = 100			# (change requires restart)
shared_buffers = 32MB
dynamic_shared_memory_type = posix	# the default is the first option
wal_level = replica			# minimal, replica, or logical
synchronous_commit = off		# synchronization level;
max_wal_size = 1GB
min_wal_size = 80MB
archive_mode = on		# enables archiving; off, on, or always
archive_command = '/bin/date' #'DATE=`date +%Y%m%d`; DIR=/home/postgres/archive/$DATE; (test -d $DIR || mkdir -p $DIR) & cp %p $DIR/%f'
restore_command = 'cp /home/postgres/archive/20200403/%f %p;'   # 'cp /home/postgres/pgbak/pg_wal/%f %p'
max_wal_senders = 10		# max number of walsender processes
wal_keep_segments = 256		# in logfile segments; 0 disables
synchronous_standby_names = '*'	# standby servers that provide sync rep
log_timezone = 'Asia/Shanghai'
datestyle = 'iso, mdy'
timezone = 'Asia/Shanghai'
lc_messages = 'en_US.UTF-8'			# locale for system error message
lc_monetary = 'en_US.UTF-8'			# locale for monetary formatting
lc_numeric = 'en_US.UTF-8'			# locale for number formatting
lc_time = 'en_US.UTF-8'				# locale for time formatting
default_text_search_config = 'pg_catalog.english'
shared_preload_libraries = 'pgmemcache'	# (change requires restart)
pgmemcache.default_servers = '127.0.0.1:11211' # multiple memcached separated bt comma ,
pgmemcache.default_behavior = 'BINARY_PROTOCOL:1' # multiple setting separated  by comma ,
```



#### pg_hba.conf

```properties
host     replication     replica             127.0.0.1/32            md5
```

#### Replication user

```sql
create role replica login replication encrypted  password 'replica';
```



### Create Slave

#### Create PGDATA2 for slave

```shell
sudo mkdir /usr/local/pgsql/data2
sudo chown postgres /usr/local/pgsql/data2
# no need initdb as we will
#/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data2
#/usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data2 >logfile 2>&1 &
```

#### Backup master to slave

```shell
# as slave table space /home/postgres/tmp will use the same path as master, and it could not be empty.
# we need rename it, the backup will create new one /home/postgres/tmp
mv /home/postgres/tmp /home/postgres/tmp1
pg_basebackup -F p -D $PGDATA2 -h 127.0.0.1 -p 5432 -U replica
```

Config - postgresql.conf

```properties
# to avoid conflict with master
port = 5433
recovery_target_timeline = 'latest' 
primary_conninfo = 'host=127.0.0.1 port=5432 user=replica' 

hot_standby = on                        # "off" disallows queries during recovery
                                        # (change requires restart)
max_standby_archive_delay = 30s # max delay before canceling queries
                                        # when reading WAL from archive;
                                        # -1 allows indefinite delay
max_standby_streaming_delay = 30s       # max delay before canceling queries
                                        # when reading streaming WAL;
                                        # -1 allows indefinite delay
wal_receiver_status_interval = 10s      # send replies at least this often
                                        # 0 disables
hot_standby_feedback = on               # send info from standby to prevent
                                        # query conflicts
wal_receiver_timeout = 60s              # time that receiver waits for
                                        # communication from master
                                        # in milliseconds; 0 disables
wal_retrieve_retry_interval = 5s        # time to wait before retrying to
```

full version:

```properties
port = 5433				# (change requires restart)
max_connections = 100			# (change requires restart)
shared_buffers = 32MB
dynamic_shared_memory_type = posix	# the default is the first option
wal_level = replica			# minimal, replica, or logical
synchronous_commit = on 		# synchronization level;
max_wal_size = 1GB
min_wal_size = 80MB
recovery_target_timeline = 'latest'	# 'current', 'latest', or timeline ID
primary_conninfo = 'host=127.0.0.1 port=5432 user=replica password=replica'			# connection string to sending server
hot_standby = on			# "off" disallows queries during recovery
max_standby_archive_delay = 30s	# max delay before canceling queries
max_standby_streaming_delay = 30s	# max delay before canceling queries
wal_receiver_status_interval = 10s	# send replies at least this often
hot_standby_feedback = on		# send info from standby to prevent
wal_receiver_timeout = 60s		# time that receiver waits for
wal_retrieve_retry_interval = 5s	# time to wait before retrying to
log_timezone = 'Asia/Shanghai'
datestyle = 'iso, mdy'
timezone = 'Asia/Shanghai'
lc_messages = 'en_US.UTF-8'			# locale for system error message
lc_monetary = 'en_US.UTF-8'			# locale for monetary formatting
lc_numeric = 'en_US.UTF-8'			# locale for number formatting
lc_time = 'en_US.UTF-8'				# locale for time formatting
default_text_search_config = 'pg_catalog.english'
shared_preload_libraries = 'pgmemcache'	# (change requires restart)
pgmemcache.default_servers = '127.0.0.1:11211' # multiple memcached separated bt comma ,
pgmemcache.default_behavior = 'BINARY_PROTOCOL:1' # multiple setting separated  by comma ,
```



#### create standby.conf

```shell
touch standby.signal
```

#### Start up slave

```shell
pg_ctl start -D $PGDATA2
```

```shell
# below message can be found in slave
2020-04-04 21:48:17.798 CST [2157] LOG:  started streaming WAL from primary at 0/4D000000 on timeline 4

# below message can be found in master
2020-04-04 21:48:17.854 CST [2158] LOG:  standby "walreceiver" is now a synchronous standby with priority 1

# check the process can see the stream
top -c -u postgres
 2158 postgres  20   0   83832   6884   5768 S   0.0  0.1   0:00.00 postgres: walsender replica 127.0.0.1(59718) streaming 0/4D0126B0  
```

Now any changes made in primary will be sync to slave.

### Switch master and slave roles

#### stop master

#### ifdown <master_ip>

#### promote slave

```
pg_ctl promote
```

#### ifup <slave_ip>

#### update master conf as slave one

#### touch standby.signal on master

#### pg_controldata to check state

### Some notes

#### synchronous_commit

If master on, then slave must be started up, otherwise all the operations on master can't be committed.

If On, performance will be much worse.

#### pg_state_replication

```sql
postgres=# \x
Expanded display is on.
postgres=# select * from pg_stat_replication ;
-[ RECORD 1 ]----+------------------------------
pid              | 14510
usesysid         | 32877
usename          | replica
application_name | walreceiver
client_addr      | 127.0.0.1
client_hostname  | 
client_port      | 49508
backend_start    | 2020-04-05 10:06:00.9904+08
backend_xmin     | 575
state            | streaming
sent_lsn         | 0/4E016300
write_lsn        | 0/4E016300
flush_lsn        | 0/4E016300
replay_lsn       | 0/4E016300
write_lag        | 
flush_lag        | 
replay_lag       | 
sync_priority    | 1
sync_state       | sync
reply_time       | 2020-04-05 10:17:02.561327+08
```

sync_state = sync: this is because we set synchronous_standby_names = '*'
if synchronous_standby_names = '' then sync_state = async, in this case, even synchronous_commit=on, it won't wait for sync to slave and can commit immediately. And if slave is down, there will have no record in pg_stat_replication.

#### wal related functions

```sql
postgres=# \df *pg_current*
List of functions
-[ RECORD 1 ]-------+--------------------------
Schema              | pg_catalog
Name                | pg_current_logfile
Result data type    | text
Argument data types | 
Type                | func
-[ RECORD 2 ]-------+--------------------------
Schema              | pg_catalog
Name                | pg_current_logfile
Result data type    | text
Argument data types | text
Type                | func
-[ RECORD 3 ]-------+--------------------------
Schema              | pg_catalog
Name                | pg_current_wal_flush_lsn
Result data type    | pg_lsn
Argument data types | 
Type                | func
-[ RECORD 4 ]-------+--------------------------
Schema              | pg_catalog
Name                | pg_current_wal_insert_lsn
Result data type    | pg_lsn
Argument data types | 
Type                | func
-[ RECORD 5 ]-------+--------------------------
Schema              | pg_catalog
Name                | pg_current_wal_lsn
Result data type    | pg_lsn
Argument data types | 
Type                | func

postgres=# select pg_current_wal_flush_lsn();
-[ RECORD 1 ]------------+-----------
pg_current_wal_flush_lsn | 0/4E016300
```

4E016300 matches the one in pg_state_replication which means all changes have been sync.

```sql
postgres=# select pg_current_wal_flush_lsn(), * from pg_stat_replication;
-[ RECORD 1 ]------------+-----------------------------
pg_current_wal_flush_lsn | 0/4E016300
pid                      | 14510
usesysid                 | 32877
usename                  | replica
application_name         | walreceiver
client_addr              | 127.0.0.1
client_hostname          | 
client_port              | 49508
backend_start            | 2020-04-05 10:06:00.9904+08
backend_xmin             | 575
state                    | streaming
sent_lsn                 | 0/4E016300
write_lsn                | 0/4E016300
flush_lsn                | 0/4E016300
replay_lsn               | 0/4E016300
write_lag                | 
flush_lag                | 
replay_lag               | 
sync_priority            | 1
sync_state               | sync
reply_time               | 2020-04-05 10:27:33.94082+08
```

