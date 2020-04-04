

### Create Slave

```shell
sudo mkdir /usr/local/pgsql/data2
sudo chown postgres /usr/local/pgsql/data2
/usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data2
/usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data2 >logfile 2>&1 &
```



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

hot_standby = on    
                                        # "off" disallows queries during recovery
                                        # (change requires restart)
max_standby_archive_delay = 30s
                                        # max delay before canceling queries
                                        # when reading WAL from archive;
                                        # -1 allows indefinite delay
max_standby_streaming_delay = 30s
                                        # max delay before canceling queries
                                        # when reading streaming WAL;
                                        # -1 allows indefinite delay
wal_receiver_status_interval = 10s
                                        # send replies at least this often
                                        # 0 disables
```

#### pg_hba.conf

```properties
host     replication     replica             127.0.0.1/32            md5
```

#### Replication user

```sql
create role replica login replication encrypted  password 'replica';
```

