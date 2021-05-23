pandas_to_snowflake
=============

This is a python Package meant to making it easier for uploading dataframe to snowflake tables.

Installation
------------

To install the latest Pypi version, you’ll need to execute:

``` r
    pip install pandas_to_snowflake
    or
    python3 -m pip install pandas_to_snowflake
```

If instead you want to install the latest github master version:

``` r
    git clone https://github.com/nit567esh/pandas_to_snowflake.git
    cd <pkg_directory>
    python3 setup.py install
```

Drivers
-------
This library uses **snowflake.connector** for connecting to Snowflake.

Usage
-----

You’ll have available 3 functions fro different kind of operations:
`1. sf_create` - You can create a table from scratch from python and upload the contents of the data frame.
`2. sf_append` - You can insert/append the contents of the pandas data frame into existing snowflake table.
`3. sf_upsert` - You can insert and update the existing snowflake table using contents of the pandas data frame.

``` r
# Step 1: Import package 
import pandas_to_snowflake as ps

# Step 2: Configure snowflake authentication
snowflake_auth=(user, password, account, warehouse, database, port)

# Step 3: Use sf_create, sf_append or sf_upsert
sf_create(snowflake_auth, sql_ddl)
    Example - ps.sf_create(snowflake_auth = snowflake_auth, 
             sql_ddl = "create table test (custkey number default null, orderdate date default null)")

sf_append(dataframe, snowflake_auth, schema, table)
    Example - ps.sf_append(dataframe=iris, snowflake_auth = snowflake_auth, schema = 'analytics', table = 'iris'")

sf_upsert(dataframe, snowflake_auth, schema, table, upsertkey=('cols',....))
    Example - ps.sf_upsert(dataframe=order, snowflake_auth = snowflake_auth, schema = 'analytics', table='order', upsertkey=('date','product',))

```
