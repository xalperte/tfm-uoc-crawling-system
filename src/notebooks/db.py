# -*- coding: utf-8 -*
# Copyright (c) 2019 BuildGroup Data Services Inc.
# All rights reserved.
# This software is proprietary and confidential and may not under
# any circumstances be used, copied, or distributed.
import random

try:
    from dse.cqlengine.models import Model
    from dse.cqlengine import columns
    from dse.cqlengine.management import \
        create_keyspace_simple, sync_table as cqlengine_sync_table
    from dse.cqlengine.connection import register_connection
except ImportError:
    from cassandra.cqlengine.models import Model
    from cassandra.cqlengine import columns
    from cassandra.cqlengine.management import \
        create_keyspace_simple, sync_table as cqlengine_sync_table
    from cassandra.cqlengine.connection import register_connection

try:
    from dse.cluster import Cluster, NoHostAvailable
    from dse.auth import DSEPlainTextAuthProvider
except ImportError:
    from cassandra.cluster import Cluster, NoHostAvailable
    from cassandra.auth import DSEPlainTextAuthProvider

from pyspark.sql.types import StringType, DateType, TimestampType
from pyspark.sql.types import FloatType, DecimalType, DoubleType
from pyspark.sql.types import IntegerType


def create_cassandra_model(schema, table_name, primary_colums=None):
    class MyModel(object):
        pass

    if not isinstance(primary_colums, list):
        primary_colums = [primary_colums]

    df_fields = {}
    for field in schema.fields:
        df_fields[field.name] = field

    metadata = {
        "__table_name__": table_name
    }

    # First the primary keys
    for field_name in primary_colums:
        field = df_fields[field_name]
        if isinstance(field.dataType, StringType):
            metadata[field_name] = columns.Text(required=(not field.nullable),
                                                primary_key=True)
        if isinstance(field.dataType, DateType):
            metadata[field_name] = columns.Date(required=(not field.nullable),
                                                primary_key=True)
        if isinstance(field.dataType, TimestampType):
            metadata[field_name] = columns.DateTime(
                required=(not field.nullable), primary_key=True)
        if isinstance(field.dataType, DoubleType):
            metadata[field_name] = columns.Double(
                required=(not field.nullable), primary_key=True)
        if isinstance(field.dataType, DecimalType):
            metadata[field_name] = columns.Decimal(
                required=(not field.nullable), primary_key=True)
        if isinstance(field.dataType, FloatType):
            metadata[field_name] = columns.Float(required=(not field.nullable),
                                                 primary_key=True)
        if isinstance(field.dataType, IntegerType):
            metadata[field_name] = columns.Integer(
                required=(not field.nullable), primary_key=True)

    # First the primary keys
    for field_name, field in df_fields.items():
        if field_name not in primary_colums:
            if isinstance(field.dataType, StringType):
                metadata[field_name] = columns.Text(
                    required=(not field.nullable), primary_key=False)
            if isinstance(field.dataType, DateType):
                metadata[field_name] = columns.Date(
                    required=(not field.nullable), primary_key=False)
            if isinstance(field.dataType, TimestampType):
                metadata[field_name] = columns.DateTime(
                    required=(not field.nullable), primary_key=False)
            if isinstance(field.dataType, DoubleType):
                metadata[field_name] = columns.Double(
                    required=(not field.nullable), primary_key=False)
            if isinstance(field.dataType, DecimalType):
                metadata[field_name] = columns.Decimal(
                    required=(not field.nullable), primary_key=False)
            if isinstance(field.dataType, FloatType):
                metadata[field_name] = columns.Float(
                    required=(not field.nullable), primary_key=False)
            if isinstance(field.dataType, IntegerType):
                metadata[field_name] = columns.Integer(
                    required=(not field.nullable), primary_key=False)

    return type('MyModel', (Model,), metadata)


def sync_table(df, dse_host, keyspace, table_name, primary_columns=None):
    cluster = None

    try:
        conn_name = f"my_connection_{random.random()}"

        cluster = Cluster([dse_host])  # provide contact points and port
        session = cluster.connect()
        register_connection(conn_name, session=session)

        # Create the keyspace if it does not exists
        create_keyspace_simple(keyspace, 1, connections=[conn_name])

        # Attach the keyspace to the session.
        session.set_keyspace(keyspace)

        # Prepare a model class mimicking the structure
        # of the dataframe (fields)
        model = create_cassandra_model(df.schema, table_name, primary_columns)
        register_connection(conn_name, session=session)
        # Create the table in cassandra using the model (cqlengine)
        cqlengine_sync_table(
            model, keyspaces=[keyspace], connections=[conn_name])

        try:
            session.execute(f"create search index on {keyspace}.{table_name}")
        except:
            # Maybe the index is already in place
            pass
    finally:
        print("Closing connections")
        if cluster:
            cluster.shutdown()
