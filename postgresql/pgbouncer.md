## pgbouncer 

- Lightweight connection pooler for PostgreSQL
- 2k memory per connection
- 3 modes

  - session
  - transaction
  - statement

### install

- pgbouncer package:

  https://www.pgbouncer.org/
  or https://github.com/pgbouncer/pgbouncer

#### install libevent

```shell
# http://libevent.org/
wget https://github.com/libevent/libevent/releases/download/release-2.1.11-stable/libevent-2.1.11-stable.tar.gz
tar -zxvf libevent-2.1.11-stable.tar.gz
cd libevent-2.1.11-stable/
./configure --prefix=/usr
make
sudo make install
echo "/usr/local/lib" >> /etc/ld.so.conf
# 检测安装是否成功
ls -al /usr/lib | grep libevent
ldconfig -p | grep libevent
ldconfig -p | grep ares # 异步DNS请求库 c-ares
```

#### install pgbouncer

```shell
cd pgbouncer-1.12.0/
./configure --prefix=/usr/local
make
su
make install
```

### config

#### config.ini

```properties
[databases]
aliasdb1=host=127.0.0.1 port=5432 dbname=test pool_size=5
[pgbouncer]
pool_mode=transaction
listen_port=6543
listen_addr=0.0.0.0
auth_type=md5
auth_file=/home/postgres/pgbouncer-1.12.0/etc/users.txt
logfile = /home/postgres/pgbouncer-1.12.0/etc/pgbouncer.log
pidfile =/home/postgres/pgbouncer-1.12.0/etc/pgbouncer.pid
unix_socket_dir=/home/postgres/pgbouncer-1.12.0/etc
admin_users=pgadmin
stats_users=pgmon
server_reset_query=DISCARD ALL
server_check_query=select 1
server_check_delay=30
max_client_conn=50000
default_pool_size=20
reserve_pool_size=5
dns_max_ttl=15
```

#### Create user/role, grant right

```sql
-- create use with md5 password, if use unencrypted then plain password
create role vista login encrypted password 'vista';
grant all on database test to vista;
-- \c test vista
\c test postgres
-- get the md5 password to put into auth_file
select * from pg_shadow;
```

#### auth_file

```
"pgadmin" "pgadmin"
"pgmon" "pgmon"
"vista" "md5585642933da79dcb1b4274665862c8d3"
```

```shell
chmod 400 /home/postgres/pgbouncer-1.12.0/etc/users.txt
```



### start up pgbouncer

```shell
pgbouncer -d /home/postgres/pgbouncer-1.12.0/etc/my-config.ini
netstat -anp | grep 6543
```



### Connect

#### Connect to pgbouncer using pgadmin

```shell
# pgbouncer is the admin database, show databases can see
/usr/local/pgsql/bin/psql -h 127.0.0.1 -p 6543 -U pgadmin pgbouncer
pgbouncer=# show help;
NOTICE:  Console usage
DETAIL:  
	SHOW HELP|CONFIG|DATABASES|POOLS|CLIENTS|SERVERS|USERS|VERSION
	SHOW FDS|SOCKETS|ACTIVE_SOCKETS|LISTS|MEM
	SHOW DNS_HOSTS|DNS_ZONES
	SHOW STATS|STATS_TOTALS|STATS_AVERAGES|TOTALS
	SET key = arg
	RELOAD
	PAUSE [<db>]
	RESUME [<db>]
	DISABLE <db>
	ENABLE <db>
	RECONNECT [<db>]
	KILL <db>
	SUSPEND
	SHUTDOWN

SHOW
```

#### Connect to aliasdb1 db using vista

```shell
/usr/local/pgsql/bin/psql -h 127.0.0.1 -p 6543 -U vista aliasdb1 
```

### Connect without prompt password

```shell
cd
vi .pgpass
#*:<port>:<db>:<user>:<password>
*:6543:aliasdb1:vista:vista
chmod 400 .pgpass
```

### Bench mark test

```shell
pgbench -M prepared -n -r -f ./sql/test.sql -h /home/postgres/pgbouncer-1.12.0/etc -p 6543 -U vista -c 16 -j 4 -C -T 30 aliasdb1
ERROR:  prepared statement "P0_0" already exists
# terminate process
# select pg_terminate_backend(pid) from pg_stat_activity where pid <> pg_backend_pid();

vmstat -n 1
```

