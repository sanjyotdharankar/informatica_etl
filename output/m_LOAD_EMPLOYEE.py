from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("m_LOAD_EMPLOYEE") \
    .config("spark.jars", "/path/to/ojdbc8.jar") \  # Oracle JDBC jar
    .getOrCreate()

# JDBC connection properties
oracle_url = "jdbc:oracle:thin:@//hostname:port/service_name"
source_properties = {
    "user": "your_source_user",
    "password": "your_password",
    "driver": "oracle.jdbc.driver.OracleDriver"
}

target_properties = {
    "user": "your_target_user",
    "password": "your_password",
    "driver": "oracle.jdbc.driver.OracleDriver"
}

# 🔍 Read from EMPLOYEE_SOURCE
employee_df = spark.read.jdbc(
    url=oracle_url,
    table="EMPLOYEE_SOURCE",
    properties=source_properties
)

# 🧪 Source Qualifier Transformation (SQ_EMPLOYEE)
# In this case, it's just passing through the columns.
sq_employee_df = employee_df.select("EMP_ID", "EMP_NAME")

# 🧠 Expression Transformation (EXP_EMPLOYEE)
# No logic applied here, but if needed you could add expressions here.
exp_employee_df = sq_employee_df.select("EMP_ID", "EMP_NAME")

# 🎯 Write to EMPLOYEE_TARGET
exp_employee_df.write.jdbc(
    url=oracle_url,
    table="EMPLOYEE_TARGET",
    mode="overwrite",  # or "append", depending on requirements
    properties=target_properties
)

# Stop Spark session
spark.stop()
