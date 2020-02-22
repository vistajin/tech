## Cloud SQL
* OLTP, RDBMS, ACID
* MySql, PostgreSQL
* Create instance before use, not serverless
* Use Cloud Proxy to access instance is suggested
* Create instance: SQL -> Create Instance -> MySQL | PostgreSQL -> Second Generation:
  * Instance ID
  * Root password
  * Region
  * Zone
  * MySQL version
  * Storage Type: SSD | HDD
  * Storage capacity
  * Enable auto backup and high availability
* Connect to intance: gcloud beta sql connect instance-id --user=root
* Create DB: create database db-name;
* Run SQL file: gcloud beta sql connect instance-id --user=root < xxx.sql


## Cloud Spanner
* OLTP, RDBMS, ACID, GCP proprietary
* Horizontal scaling
* Structured data
* Create instance: Spanner -> Create instance:
  * Instance name
  * Instance ID
  * Configuration region
  * Nodes: recommand >=3 for production
* Create database -> Create Table (DDL or UI): interleave in another table (parent), primary key of table is inherited -> Set primary key of child table: Single Column | Composite (parent key + other keys of child table) 
~~~sql
CREATE TABLE Rating(
id STRING(25),
userId STRINg(MAX) NOT NULL,
rating FLOAT64 NOT NULL,
) PRIMARY KEY (id, userID),
INTERLEAVE IN PARENT Accomodation ON DELETE CASCADE
~~~


## Bigtable
* GCP HBase
* NoSQL
* Time series, IoT
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
* create new dataset: bq mk dataset-name
* Show datasets: bq ls
* Describe dataset: bq show dataset-name
* Describe table: bq show project-id:dataset.table
* View data in table: bq head -n 10 project-id:dataset.table
* Query data using sql: bq query "select xxx"
* Load data:
~~~
bq load --source-format=CSV dataset.table gs://xxx.txt column-name-1:data-type,column-name-2:data-type
~~~
* Export data:
~~~
bq extract dataset.table gs://xxxx/xx.txt
~~~


