# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.
import os
import sys
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import Window
import pyspark.sql.functions as F

os.environ['PYSPARK_SUBMIT_ARGS'] = \
    '--packages datastax:spark-cassandra-connector:2.4.0-s_2.11 pyspark-shell'


def init_spark_context(context_name):

    conf = SparkConf() \
        .setAppName("Factor Analysis Job") \
        .set("spark.cassandra.connection.host", "tfm_uoc_dse") \
        .set("spark.sql.dse.search.enableOptimization", "on")
    # .set("spark.sql.execution.arrow.enabled", "true") \

    spark_master = "local"
    sc = SparkContext(spark_master, context_name, conf=conf)

    sql_context = SQLContext(sc)

    return sc, sql_context


def load_and_get_table_df(sql_context, keys_space_name, table_name):
    table_df = sql_context.read \
        .format("org.apache.spark.sql.cassandra") \
        .options(table=table_name, keyspace=keys_space_name) \
        .option("spark.sql.dse.search.enableOptimization", "on") \
        .load()
    return table_df


def fillna(
        df, partition_keys, order_field,
        field_to_fill, fill_function=F.last,
        convert_nan_to_null=True, use_same_field_as_output=False):

    if convert_nan_to_null:
        df = df.withColumn(
            field_to_fill,
            F.when(F.isnan(F.col(field_to_fill)), None).
            otherwise(F.col(field_to_fill)))

    # define the window
    if partition_keys is not None:
        window = Window.partitionBy(*partition_keys) \
            .orderBy(order_field) \
            .rowsBetween(-sys.maxsize, 0)
    else:
        window = Window \
            .orderBy(order_field) \
            .rowsBetween(-sys.maxsize, 0)

    # define the forward-filled column
    if fill_function == F.last:
        filled_column = fill_function(
            df[field_to_fill], ignorenulls=True).over(window)
    else:
        filled_column = fill_function(
            df[field_to_fill]).over(window)

    output_field = field_to_fill if use_same_field_as_output \
        else f'{field_to_fill}_filled'

    # do the fill
    spark_df_filled = df.withColumn(
        output_field,
        F.when(F.col(field_to_fill).isNull(), filled_column).
        otherwise(df[field_to_fill]))

    if partition_keys is not None:
        return spark_df_filled.orderBy(order_field, *partition_keys)

    return spark_df_filled.orderBy(order_field)