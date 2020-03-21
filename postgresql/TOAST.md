### TOAST - The Oversized-Attribute Storage Technique

- Page (Block) size = 8k, > page size-> TOAST
- 行外存储
- storage type, \d+ table_name
  - plain
  - extended: 允许压缩和行外存储。一般会先压缩，如果还是太大，就会行外存储
  - externa: 禁止压缩
  - main: 允许压缩，但不许行外存储。

```sql
mydb=# \d+ t1
mydb=# \d+ t3
                                     Table "public.t3"
 Column  |  Type   | Collation | Nullable | Default | Storage  | Stats target | Description 
---------+---------+-----------+----------+---------+----------+--------------+-------------
 id      | integer |           |          |         | plain    |              | 
 title   | text    |           |          |         | extended |              | 
 content | text    |           |          |         | extended |              | 
Access method: heap

mydb=# select relname,relfilenode,reltoastrelid from pg_class where relname='t3';
 relname | relfilenode | reltoastrelid 
---------+-------------+---------------
 t3      |       16922 |         16925
(1 row)

mydb=# \d+ pg_toast.pg_toast_16922;
TOAST table "pg_toast.pg_toast_16922"
   Column   |  Type   | Storage 
------------+---------+---------
 chunk_id   | oid     | plain
 chunk_seq  | integer | plain
 chunk_data | bytea   | plain
--- insert data to content until > 8k
select chunk_id,chunk_seq,length(chunk_data) from pg_toast.pg_toast_16922;
-- 禁止压缩, >2k 行外存储
alter table blog alter content set storage external;
```

