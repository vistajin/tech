## bigtable
* GCP HBase
* NoSQL
* Columnar store, easy to add column on the fly
* Bigtable -> Create instance
  * instance name
  * instance ID
  * Instance type: production | Development
  * Cluster ID
  * Zone
  * Storage type: SSD | HDD
* Create table with Column family: create table-name, column-family
* show tables: list
* Insert data: put table-name, row-key, column-family:column-name, value
* View data: scan table-name
* Drop table: drop table-name

## Datastore
* Document database
* NoSQL
* Query execution time depends on query result, independent on size of whole dataset
* Support automic transactions
* Kind=Table, Entity=Row, Property=Field

## BigQuery
* GCP Hive: Schema-on-read
* OLAP, Analytics, warehouse
* Project -> Dataset -> Table
* Loading data: Batch loads | Streaming loads
* Query & view data: Interactive query | Batch query | Views | Partitioned tables
