  from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max as spark_max, when

# Start Spark session
spark = SparkSession.builder \
    .appName("m_Load_Latest_Account") \
    .config("spark.jars", "/path/to/sqljdbc42.jar") \  # SQL Server JDBC jar
    .getOrCreate()

# JDBC connection config
jdbc_url = "jdbc:sqlserver://hostname:port;databaseName=yourDB"
connection_properties = {
    "user": "your_user",
    "password": "your_password",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# 📥 Step 1: Read source table
account_df = spark.read.jdbc(
    url=jdbc_url,
    table="ACCOUNT",
    properties=connection_properties
)

# 🔍 Step 2: Lookup max LASTMODIFIED_DATE
max_date = account_df.agg(spark_max("LASTMODIFIED_DATE").alias("MAX_DATE")).collect()[0]["MAX_DATE"]

# 🧠 Step 3: Expression transformation (EXP_COMPARE_DATE)
account_with_flag_df = account_df.withColumn(
    "o_IS_LATEST",
    when(col("LASTMODIFIED_DATE") == max_date, 1).otherwise(0)
)

# 🔀 Step 4: Router (RTR_LATEST_RECORD) - Filter for latest records
latest_account_df = account_with_flag_df.filter(col("o_IS_LATEST") == 1)

# 📤 Step 5: Write to target table
latest_account_df.select("ID", "NAME", "PERSONAL", "LASTMODIFIED_DATE").write.jdbc(
    url=jdbc_url,
    table="DB_ACCOUNT",
    mode="overwrite",  # Or "append" based on use case
    properties=connection_properties
)

# Stop Spark session
spark.stop()
