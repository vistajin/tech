### 本地高速缓存 

#### pgfincore

- git: https://git.postgresql.org/gitweb/?p=pgfincore.git;a=summary
- github: https://github.com/klando/pgfincore

- install

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

  



- man posix_fadvise
- https://git.postgresql.org/gitweb/?p=pgfincore.git;a=summary
- 



### 异地高速缓存

- pgmemcache
- 





