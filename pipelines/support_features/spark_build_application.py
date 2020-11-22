'''
Date: 2020-11-14
Author: Vitali Lupusor

Description: PySpark instance.
'''

def build_spark(name=None, master='local', partitions=5, memory='8g', **kwargs):
    '''Build a spark application object.
    Configuration options can be provided as key-value attributes.

    Arguments:
        name (str): Application name as shown in SparkUI.
        master (str): Sets the Spark master URL to connect to, such as “local” 
                to run locally, “local[4]” to run locally with 4 cores, or 
                “spark://master:7077” to run on a Spark standalone cluster.
        partitions (int): The number of dataframe partitions. If working 
                on a cluster, increase the number of partition for better 
                performance.
        memory (str): Executor's memory.
        **kwargs (dict): Other configuration parameters.

    return (pyspark.sql.SparkSession): Spark application object.
    '''
    # Import external modules
    _pyspark = __import__('pyspark', fromlist=['SparkConf'])
    SparkConf = _pyspark.SparkConf
    _sql = __import__('pyspark.sql', fromlist=['SparkSession'])
    SparkSession = _sql.SparkSession

    # Build Spark configuration
    conf = SparkConf().setAll([
        ('spark.sql.shuffle.partitions', partitions),
        ('spark.executor.memory', memory),
        *list(kwargs.items() if kwargs else ())
    ])

    # Build PySpark session object
    spark = SparkSession.builder \
        .config(conf=conf) \
        .master(master) \
        .appName(name) \
        .getOrCreate()

    return spark
