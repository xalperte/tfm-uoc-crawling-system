# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.
import pyspark.sql.functions as F
from pyspark.sql import Window


def group_by_period(
        df,
        columns,
        columns_aliases,
        columns_agg,
        date_field="date",
        group_columns=None,
        frequency="monthly"):
    """

    :param df:
    :param columns: the list of columns we want to select
    :param columns_aliases: the list of alias for each column we want to select
    :param agg_function: the aggregation function to apply to each
        selected column
    :param date_field:
    :param group_columns: main columns to group by (in addition to the
     date field)
    :param frequency:
    :return:


    Ex. We have a DataFrame with the following schema:
            ticker StringType
            trading_date   DateType
            close  FloatType


        And we want to generate a monthly frequency version of the data set
        with the following fields:

            ticker, year, month

            first_date_of_period
            last_date_of_period
            avg_close_price

        We run the following instruction

        group_by_period(
            my_df,
            columns=["date", "date", close"],
            columns_aliases=["first_date_of_period",
                             "last_date_of_period",
                             "avg_close_price"],
            columns_agg=[F.first, F.last, F.avg],
            date_field="trading_date",
            group_columns=["ticker"],
            frequency="monthly")
    """

    aggregations = []
    for index, column in enumerate(columns):
        if columns_agg[index] == F.last:
            aggregations.append(
                columns_agg[index](F.col(column), ignorenulls=True).alias(
                    columns_aliases[index]))
        else:
            aggregations.append(
                columns_agg[index](
                    F.col(column)).alias(columns_aliases[index]))

    aggregations.append(F.last(date_field).alias(date_field))

    group_columns = group_columns if group_columns else []

    if frequency == 'monthly':
        df = df.groupBy(*group_columns,
                        F.year(date_field).alias("year"),
                        F.month(date_field).alias("month")).\
            agg(*aggregations). \
            orderBy(*group_columns, "year", "month")
    elif frequency == 'quarterly':
        df = df.groupBy(*group_columns,
                        F.year(date_field).alias("year"),
                        F.quarter(date_field).alias("quarter")).\
            agg(*aggregations). \
            orderBy(*group_columns, "year", "quarter")
    elif frequency == 'yearly':
        df = df.groupBy(*group_columns,
                        F.year(date_field).alias("year")).\
            agg(*aggregations). \
            orderBy(*group_columns, "year")

    df = df.withColumn(
        date_field, F.last_day(F.col(date_field)).alias(date_field))

    return df


def get_log_returns(
        df,
        ticker_field="ticker",
        date_field="date",
        ct_price_field="close",
        output_field=None,
        frequency="monthly"):
    """

    :param df: dataframe with the asset prices
    :param ct_price_field: the field with the current price of the asset
    :param ticker_field: the field with the name of the asset
    :param date_field: the name of the field that contains the date
        of each asset price
    :param output_field: the name of the calculated column with the log returns
    :param frequency: the period to be computed:
        daily, monthly, quarterly, yearly
    :return: the df dataframe with the new column `output_field`
    """

    if not output_field:
        output_field = f"{ct_price_field}_log_returns"

    w = Window().partitionBy(ticker_field).orderBy(date_field)

    df = df.withColumn(
        output_field,
        (F.col(ct_price_field) / F.lag(ct_price_field, 1).over(w)) - 1)

    return df


def compute_zscore(df, date_column, value_column, output_column=None):
    """
    Standardize the value column using the z-score function for a given
    date column. The z-score is being computed using all the past data points
    in the series.

    :param df: the Spark dataframe with the time series
    :param date_column: the column of the DataFrame that contains the date
     of the time series
    :param value_column: the column of the DataFrame we want to standardize
    :param output_column: the outtput column in the dataset with the result
        of the operation
    :return: the dataframe with a new column that contains the z-scored value
        for the value_column
    """

    if output_column is None:
        output_column = f"{value_column}_zscored"

    def z_score_w(col, w):
        avg_ = F.avg(col).over(w)
        avg_sq = F.avg(col * col).over(w)
        sd_ = F.sqrt(avg_sq - avg_ * avg_)
        return (col - avg_) / sd_

    w = Window().partitionBy(date_column)
    return df.withColumn(
        output_column, z_score_w(df[value_column], w))
