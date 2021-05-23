from snowflake.connector.pandas_tools import write_pandas
import pandas as pd, snowflake.connector

def sf_create(snowflake_auth, sql_ddl):
    con = snowflake.connector.connect(user=snowflake_auth[0], password=snowflake_auth[1], account=snowflake_auth[2], warehouse=snowflake_auth[3], database=snowflake_auth[4],port=snowflake_auth[5],)
    cur = con.cursor()
    cur.execute(sql_ddl)
    con.commit()
    cur.close()
    print("\x1B[3mTable created sucessfully.\x1B[23m")

def sf_append(dataframe, snowflake_auth, schema, table):
    dataframe.columns=dataframe.columns.str.upper()
    dataframe=dataframe.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    timestamp_columns = dataframe.select_dtypes(['datetime64[ns]']).columns
    for column in timestamp_columns:
        dataframe[column]=pd.to_datetime(dataframe[column]).dt.strftime("%Y-%m-%d %H:%M:%S")

    print("Started appending dataframe into snowflake table.")
    con = snowflake.connector.connect(user=snowflake_auth[0], password=snowflake_auth[1], account=snowflake_auth[2], warehouse=snowflake_auth[3], database=snowflake_auth[4],port=snowflake_auth[5],)
    cur = con.cursor()
    cur.execute("USE SCHEMA "+str(schema).upper())
    success, nchunks, nrows, _ = write_pandas(con, dataframe, table_name=table.upper(),schema=schema.upper())
    cur.close()
    con.commit()
    print(str(nrows)+ ' Rows Loaded Successfully')

def sf_upsert(dataframe, snowflake_auth, schema, table, upsertkey):        
        create = "create table "+str("temp")+str(".")+str(table)+str("  like ")+str(schema)+str(".")+str(table)
        drop="drop table if exists " +str("temp")+str(".")+str(table)
        
        print('Creating staging table.')
        con = snowflake.connector.connect(user=snowflake_auth[0], password=snowflake_auth[1], account=snowflake_auth[2], warehouse=snowflake_auth[3], database=snowflake_auth[4],port=snowflake_auth[5],)
        cur = con.cursor()
        cur.execute(drop)
        cur.execute(create)

        cur.execute("USE SCHEMA "+str("temp").upper())
        
        success, nchunks, nrows, _ = write_pandas(con, dataframe, table_name=table.replace('\"','').upper(),schema="temp".upper())

        cur.execute("select column_name from information_schema.columns where table_name=upper('"+table.replace('\"','')+"') and table_schema=upper('"+schema+"')order by ordinal_position;")
        column_name=pd.DataFrame(cur.fetchall())

        columnname = [i[0] for i in cur.description]
        column_name.columns = columnname

        print("Merging data from staging to main table.")

        target_columns=column_name['COLUMN_NAME'].to_list()
        columns=','.join([str(i) for i in target_columns])

        upsert_str=''
        if isinstance(upsertkey,tuple):
            for i in upsertkey:
                upsert_str+='Target.'+i+'=Source.'+i+' and '

        if upsert_str.endswith(' and '):
                upsert_str = upsert_str[:-5]
                
        source_columns=','.join(['Source.'+str(i) for i in target_columns])
        update_set=','.join([str(i)+'=Source.'+str(i) for i in target_columns])
        cur = con.cursor()
        cur.execute("""MERGE INTO """+schema+"""."""+table+""" as Target USING (SELECT * FROM temp."""+table+""" AS s ("""+columns+"""
            )) AS Source ON """+upsert_str+""" WHEN NOT MATCHED THEN INSERT ("""+columns+""") VALUES ("""+source_columns+""") WHEN MATCHED THEN UPDATE set """+update_set+""";""")


        print("Dropping staging table.")
        cur.execute(drop)

        print('Data upserted successfully')

        con.commit()
        cur.close()
        con.close()