import datetime
import os
import re
import psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import time
import sys

from satori import satori
from satori import satori_common

#Enter table position key to restart where it stopped, if don't know put 0
START_TBL_KEY = 0


def scan_schema(host, dbname, target_schema_name, user, password, running_mode):

	str_sql = "SELECT C.TABLE_CATALOG,C.TABLE_SCHEMA,C.TABLE_NAME,C.COLUMN_NAME,T.TABLE_TYPE FROM INFORMATION_SCHEMA.COLUMNS C INNER JOIN INFORMATION_SCHEMA.TABLES T ON C.TABLE_NAME=T.TABLE_NAME WHERE (C.TABLE_SCHEMA) = '{}';".format(target_schema_name)
  		

	con = psycopg2.connect(dbname=dbname, user=user,  host=host, password=password)

	print("Running scanner")
	tables = []
	views = []
	table_columns = []
	view_columns = []
	key_counter = 0
	cur = con.cursor()
	print (str_sql)
	cur.execute(str_sql)
	print("Populating tables")
	rows = cur.fetchall()
	for record in rows:
		print(record)
		table_name = record[2]
		db_name = record[0]
		schema_name = record[1]
		column_name = record[3]
		table_type = record[4]
		if (schema_name == target_schema_name):
			fully_qualified_location = "\"{}\".\"{}\".\"{}\"".format(db_name.replace("\"", "\"\""), schema_name.replace("\"", "\"\""), table_name.replace("\"", "\"\""))
			key_counter=key_counter+1
			if table_type == 'BASE TABLE':
				if fully_qualified_location not in table_columns:
					tables.append(fully_qualified_location)
				table_columns.append({"table": fully_qualified_location, "column": column_name,"key":key_counter})
			elif table_type == 'VIEW':
				if fully_qualified_location not in views:
					views.append(fully_qualified_location)
				view_columns.append({"view": fully_qualified_location, "column": column_name,"key":key_counter})
	 
			for column in table_columns:

				 if running_mode == "wet" and START_TBL_KEY == 0:
#						print("Querying {}.{} at position {}".format(column["table"], column["column"],column["key"]))
						str_sql = "SELECT '{}' FROM {} WHERE '{}' IS NOT NULL AND LENGTH(TRIM('{}'::text)) > 0 LIMIT 300;".format(column["column"],column["table"],column["column"],column["column"])
						con.cursor().execute(str_sql)
				 else:
					 if running_mode == "dry" and START_TBL_KEY == 0:
						 print("Querying {}.{} at position {}".format(column["table"], column["column"],column["key"]))
						 str_sql = "SELECT {} FROM {} WHERE {} IS NOT NULL AND LENGTH(TRIM({}::text)) > 0 LIMIT 300;".format(column["column"],column["table"], column["column"],column["column"])

			for column in view_columns:

				 if running_mode == "wet" and START_TBL_KEY == 0:
#						print("Querying {}.{} at position {}".format(column["view"], column["column"],column["key"]))
						str_sql = "SELECT {} FROM {} WHERE {} IS NOT NULL AND LENGTH(TRIM({}::text)) > 0 LIMIT 300;".format(column["column"],column["view"], column["column"],column["column"])
						#print (str_sql)
						con.cursor().execute(str_sql)
				 else:
					 if running_mode == "dry" and START_TBL_KEY == 0:
						 print("Querying {}.{} at position {}".format(column["view"], column["column"],column["key"]))
						 str_sql = "SELECT {} FROM {} WHERE {} IS NOT NULL AND LENGTH(TRIM({}::text)) > 0 LIMIT 300;".format(column["column"],column["view"], column["column"],column["column"])

