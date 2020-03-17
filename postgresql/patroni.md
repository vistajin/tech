

- patroni.yml

  ```yaml
  scope: postgres-cluster
  name: pgnode01
  namespace: /service/
   
  restapi:
    listen: 192.168.216.130:8008
    connect_address: 192.168.216.130:8008
  #  certfile: /etc/ssl/certs/ssl-cert-snakeoil.pem
  #  keyfile: /etc/ssl/private/ssl-cert-snakeoil.key
  #  authentication:
  #    username: username
  #    password: password
   
  etcd:
    hosts: 192.168.216.130:2379,192.168.216.132:2379,192.168.216.134:2379
   
  bootstrap:
    # this section will be written into Etcd:/<namespace>/<scope>/config after initializing new cluster
    # and all other cluster members will use it as a `global configuration`
    dcs:
      ttl: 30
      loop_wait: 10
      retry_timeout: 10
      maximum_lag_on_failover: 1048576
      master_start_timeout: 300
      synchronous_mode: false
      synchronous_mode_strict: false
      #standby_cluster:
        #host: 127.0.0.1
        #port: 1111
        #primary_slot_name: patroni
      postgresql:
        use_pg_rewind: true
        use_slots: true
        parameters:
          max_connections: 100
          superuser_reserved_connections: 5
          max_locks_per_transaction: 64
          max_prepared_transactions: 0
          huge_pages: try
          shared_buffers: 512MB
          work_mem: 128MB
          maintenance_work_mem: 256MB
          effective_cache_size: 4GB
          checkpoint_timeout: 15min
          checkpoint_completion_target: 0.9
          min_wal_size: 2GB
          max_wal_size: 4GB
          wal_buffers: 32MB
          default_statistics_target: 1000
          seq_page_cost: 1
          random_page_cost: 4
          effective_io_concurrency: 2
          synchronous_commit: on
          autovacuum: on
          autovacuum_max_workers: 5
          autovacuum_vacuum_scale_factor: 0.01
          autovacuum_analyze_scale_factor: 0.02
          autovacuum_vacuum_cost_limit: 200
          autovacuum_vacuum_cost_delay: 20
          autovacuum_naptime: 1s
          max_files_per_process: 4096
          archive_mode: on
          archive_timeout: 1800s
          archive_command: cd .
          wal_level: replica
          wal_keep_segments: 130
          max_wal_senders: 10
          max_replication_slots: 10
          hot_standby: on
          wal_log_hints: on
          shared_preload_libraries: pg_stat_statements,auto_explain
          pg_stat_statements.max: 10000
          pg_stat_statements.track: all
          pg_stat_statements.save: off
          auto_explain.log_min_duration: 10s
          auto_explain.log_analyze: true
          auto_explain.log_buffers: true
          auto_explain.log_timing: false
          auto_explain.log_triggers: true
          auto_explain.log_verbose: true
          auto_explain.log_nested_statements: true
          track_io_timing: on
          log_lock_waits: on
          log_temp_files: 0
          track_activities: on
          track_counts: on
          track_functions: all
          log_checkpoints: on
          logging_collector: on
          log_truncate_on_rotation: on
          log_rotation_age: 1d
          log_rotation_size: 0
          log_line_prefix: '%t [%p-%l] %r %q%u@%d '
          log_filename: 'postgresql-%a.log'
          log_directory: /var/log/postgresql
    
   #      recovery_conf:
  #        restore_command: cp ../wal_archive/%f %p
    
    # some desired options for 'initdb'
    initdb:  # Note: It needs to be a list (some options need values, others are switches)
    - encoding: UTF8
    - locale: en_US.UTF-8
    - data-checksums
    
    pg_hba:  # Add following lines to pg_hba.conf after running 'initdb'
    - host replication replicator 0.0.0.0/0 md5
    - host all all 0.0.0.0/0 md5
   
   # Additional script to be launched after initial cluster creation (will be passed the connection URL as parameter)
  # post_init: /usr/local/bin/setup_cluster.sh
    
    # Some additional users which needs to be created after initializing new cluster
  #  users:
  #    admin:
  #      password: admin-pass
  #      options:
  #        - createrole
  #        - createdb
   
     
  postgresql:
    listen: 192.168.216.130,127.0.0.1:5432
    connect_address: 192.168.216.130:5432
    use_unix_socket: true
    data_dir: /var/lib/pgsql/11/data
    bin_dir: /usr/pgsql-11/bin
    config_dir: /var/lib/pgsql/11/data
    pgpass: /var/lib/pgsql/.pgpass
    authentication:
      replication:
        username: replicator
        password: replicator-pass
      superuser:
        username: postgres
        password: postgres-pass
  #    rewind:  # Has no effect on postgres 10 and lower
  #      username: rewind_user
  #      password: rewind_password
    parameters:
      unix_socket_directories: /var/run/postgresql
      stats_temp_directory: /var/lib/pgsql_stats_tmp
    
  #  callbacks:
  #    on_start:
  #    on_stop:
  #    on_restart:
  #    on_reload:
  #    on_role_change:
    
    create_replica_methods:
  #   - pgbackrest
  #   - wal_e
     - basebackup
  # pgbackrest:
  #   command: /usr/bin/pgbackrest --stanza=<Stanza_Name> --delta restore
  #   keep_data: True
  #   no_params: True
  #  wal_e
  #    command: patroni_wale_restore
  #    no_master: 1
  #    envdir: /etc/wal_e/envdir
  #    use_iam: 1
    basebackup:
      max-rate: '100M'
    
   #watchdog:
  #  mode: automatic # Allowed values: off, automatic, required
  #  device: /dev/watchdog
  #  safety_margin: 5
    
  tags:
      nofailover: false
      noloadbalance: false
      clonefrom: false
      nosync: false
  # specify a node to replicate from. This can be used to implement a cascading replication.
  #    replicatefrom: (node name)
  ```

  