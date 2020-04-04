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
#synchronous_standby_names = ''
# suggest
archive_mode = on
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