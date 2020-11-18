'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: TODO
'''

def build_spark(name=None, master='local', partitions=5, memory='8g'):
    '''TODO

    Arguments:
        arg (): TODO

    return (): TODO
    '''
    # Import external modules
    _pyspark = __import__('pyspark', fromlist=['SparkConf'])
    SparkConf = _pyspark.SparkConf
    _sql = __import__('pyspark.sql', fromlist=['SparkSession'])
    SparkSession = _sql.SparkSession

    # Build Spark configuration
    conf = SparkConf().setAll([
        ('spark.sql.shuffle.partitions', partitions),
        ('spark.executor.memory', memory) # ,
        # ('spark.mongodb.input.uri', ''),
        # ('spark.mongodb.output.uri', '')
    ])

    # Build PySpark session object
    spark = SparkSession.builder \
        .config(conf=conf) \
        .master(master) \
        .appName(name) \
        .getOrCreate()

    return spark
