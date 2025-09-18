# Databricks notebook source
# MAGIC %md
# MAGIC ### Importing CSV Data Files

# COMMAND ----------

sales_df = spark.read.csv("/FileStore/tables/sales_data.csv", header=True, inferSchema=True)
store_df = spark.read.csv("/FileStore/tables/store_data.csv", header=True, inferSchema=True)
display(sales_df)
display(store_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Data Cleaning

# COMMAND ----------

# DBTITLE 1,Cleaning of Sales data
#### We have to clean the sales data by removing null values, duplicates and negative values ####

from pyspark.sql.functions import *

#fillna() is used for filling '0' to the null values of the specified mentioned columns in table, by adding values into dictionary form.
sales_df = sales_df.fillna({"quantity":0, "total_amount":0})

#Removing Null Values from sale_id, store_id, sale_date columns
sales_df = sales_df.filter((col("sale_id").isNotNull()) & (col("store_id").isNotNull()) & (col("sale_date").isNotNull()))

#Removing negative values from quantity and total_amount columns
sales_df = sales_df.filter((col("quantity") > 0) & (col("total_amount") > 0))

#dropDuplicates() is used for dropping the duplicate rows in the table
sales_df = sales_df.dropDuplicates()

display(sales_df)

# COMMAND ----------

display(store_df)

# COMMAND ----------

# DBTITLE 1,Cleaning the Store Data
from pyspark.sql.functions import avg, col

#Removing the null values from store_id
store_df = store_df.filter(col("store_id").isNotNull())

#.first()[0] is used for getting the first value of the column store_size.
avg_store_df = store_df.select(avg("store_size")).first()[0]
print(avg_store_df)

#Now, we have to replace the null values of store_size with store_size's average size.
store_df = store_df.fillna({"store_size": avg_store_df})

#Now, we have to remove null values from open_date column
store_df = store_df.filter(col("open_date").isNotNull())

display(store_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Data Transformation

# COMMAND ----------

#Joining both the data frames together

combined_df = sales_df.join(store_df, on="store_id", how="inner")
display(combined_df)

# COMMAND ----------

#Adding new column for sales per square foot
from pyspark.sql.functions import year, col, round
combined_df = combined_df.withColumn("year", year(col("sale_date")))
combined_df = combined_df.withColumn("sales_per_sqrft", round(col("total_amount") / col("store_size"),2))
display(combined_df)

# COMMAND ----------

#To calculate the total sales and total quantity per store and region.
#createOrReplaceTempView() is used for creating a temporary view of the table
combined_df.createOrReplaceTempView("combined")

store_sales_sql = spark.sql("""
    SELECT 
        store_id, 
        store_region, 
        SUM(total_amount) as total_sales, 
        SUM(quantity) as total_quantity 
    FROM combined 
    GROUP BY store_id, store_region
""")

display(store_sales_sql)

# COMMAND ----------

#To find the top 5 product sold by total_quantity sold.
top_products_sql = spark.sql("""
        Select
            product_id,
            SUM(quantity) as total_quantity
        FROM combined
        GROUP BY product_id
        ORDER BY total_quantity DESC  
        LIMIT 5
""")

display(top_products_sql)


# COMMAND ----------

#To find top 5 stores by sales
store_sales_sql.createOrReplaceTempView("store_sales")
top_stores = spark.sql("""
    SELECT
       store_id,
       total_sales from store_sales
    ORDER BY total_sales DESC
    LIMIT 5                                       
""")

display(top_stores)

# COMMAND ----------

# DBTITLE 1,Loading the files into the DBFS
#Storing them into parquet files format into the DBFS
top_products_sql.write.mode("overwrite").parquet("/FileStore/tables/top_products")
top_stores.write.parquet("/FileStore/tables/top_stores")

# COMMAND ----------

# MAGIC %fs
# MAGIC ls /FileStore/tables