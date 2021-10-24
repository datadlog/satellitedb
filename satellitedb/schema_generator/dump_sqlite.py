# MIT License
# Copyright (c) 2021 Data Dlog

"""
Purpose

This module generates the DDL's for SQLite database objects. 
"""

import io
import logging
import os
import sqlite3

logger = logging.getLogger(__name__)


def connection(db_url):
    """This method, builds the connection to connect SQLite database
    Args:
        param db_url: Database file URL
    Returns:
        value: Return the connection details as object
    Raises:
        OperationalError: if database URL not exists
    """
    try:
        conn = sqlite3.connect(db_url)
        return conn
    except Exception as msg:
        logger.error("Unable to open database file")
        raise Exception(msg)


def create_directory(tar_loc, obj_type):
    """This method, create the directory for each object from the list.
    Args:
        param tar_loc: Target loation to dump the files.
        param obj_type: Database object type like tables, views etc..
    Returns:
        value: Return the path of object location
    Raises:
        Raise an error if Build script fails
    """
    try:
        path = os.path.join(tar_loc, obj_type)
        logger.info("Checking target diretory exists or not - {}".format(path))
        is_exist = os.path.exists(path)

        if not is_exist:
            logger.info("Target diretory not exists, creating - {}".format(path))
            os.makedirs(path)
        return path
    except Exception as msg:
        logger.error("Creating directory failed")
        raise Exception(msg)


def create_ddl(obj_type):
    """This method, create the DDLs script for each object from the list.
    Args:
        param obj_type: Database object type like tables, views etc..
    Returns:
        value: Return the SQL statement
    Raises:
        Raise an error if Build script fails
    """
    try:
        logger.info("Creating DDL script for - {}".format(obj_type))

        query = """
            SELECT "name", "type", "sql"
            FROM "sqlite_master"
                WHERE "sql" NOT NULL AND
                "type" == '{}'
                ORDER BY "name"
            """.format(
            obj_type,
        )
        return query
    except Exception as msg:
        logger.error("Creating DDL script failed")
        raise Exception(msg)


def create_objects(response, tar_loc, file_extn, obj_type):
    """This method, create the DDLs and dumps to given location.
    Args:
        param response: its an object, contains all the db objects DDLs
        param tar_loc: Target location to dump the files
        param file_extn: File extension like .sql, .txt
        param obj_type: Database object type like tables, views etc..
    Returns:
        None:
    Raises:
        Raise an error if schema generator fails
    """
    try:
        if response:
            path = create_directory(tar_loc, obj_type)
            logger.info("Exporting all the {} DDL".format(obj_type))

            for _, schema in enumerate(response.fetchall(), start=0):
                file_name = "{}.{}".format(str(schema[0]).lower(), file_extn)
                file_path = os.path.join(tar_loc, obj_type, file_name)

                with open(file_path, "wb+") as file:
                    buffer = io.BytesIO()
                    buffer.write(str(schema[2]).encode("utf-8"))
                    buffer.write(b";\n")
                    file.write(buffer.getvalue())
            logger.info("All the {} DDL are exported to {}".format(obj_type, path))
    except Exception as msg:
        logger.error("Create DDLs failed for SQLite database")
        raise Exception(msg)


def main(db_url, tar_loc, file_extn, incl_db_objs):
    """Main method, runs for SQLite database type
    Args:
        param db_url: Database URL
        param tar_loc: Target location to dump the files
        param file_extn: File extension like .sql, .txt
        param incl_db_objs: Database objects
    Returns:
        None:
    Raises:
        Raise an error if schema generator fails
    """
    logger.info("Starts Connecting database")
    conn = connection(db_url)
    cursor = conn.cursor()
    logger.info("Database connected")

    if "tables" in incl_db_objs:
        logger.info("Starts activity for tables")
        query = create_ddl("table")
        response = cursor.execute(query)
        create_objects(response, tar_loc, file_extn, "tables")
        logger.info("Ends activity for tables")

    if "views" in incl_db_objs:
        logger.info("Starts activity for views")
        query = create_ddl("view")
        response = cursor.execute(query)
        create_objects(response, tar_loc, file_extn, "views")
        logger.info("Ends activity for views")

    if "indexes" in incl_db_objs:
        logger.info("Starts activity for indexes")
        query = create_ddl("index")
        response = cursor.execute(query)
        create_objects(response, tar_loc, file_extn, "indexes")
        logger.info("Ends activity for indexes")

    if "triggers" in incl_db_objs:
        logger.info("Starts activity for triggers")
        query = create_ddl("trigger")
        response = cursor.execute(query)
        create_objects(response, tar_loc, file_extn, "triggers")
        logger.info("Ends activity for triggers")
