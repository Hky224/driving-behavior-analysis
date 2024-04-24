from pyspark import SparkContext
import sys

# Initialize a SparkContext

sc = SparkContext()



out = "s3://comp4442-gp/output/"



# Read all files at once into a single RDD  
rdd = sc.wholeTextFiles("s3://comp4442-gp/input/")
def safe_int(x):
    try:
        return int(x) if x is not None else 0
    except ValueError:
        return 0

records = rdd.flatMap(lambda file: file[1].split("\n")).map(lambda line: line.split(",")).filter(lambda line: len(line)>8)


# Map each line to a tuple with the driverID, day, and hour as the key and the other fields as the value
key_value = records.map(lambda p: ((p[0],  p[1], p[7]),  [safe_int(x) for x in p[8:19]]))
# Reduce by key to sum up the values for each key
result = key_value.reduceByKey(lambda a, b: [x + y for x, y in zip(a, b)])


result.saveAsTextFile(out)
sc.stop()