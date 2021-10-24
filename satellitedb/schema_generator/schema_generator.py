# MIT License
# Copyright (c) 2021 Data Dlog

"""
Purpose

This module initiates the process for each database schema generation. 
"""


import logging

from . import dump_sqlite

logger = logging.getLogger(__name__)


def main(db_type, db_url, tar_loc, file_extn, incl_db_objs):
    """Main method, runs for each database type
    Args:
        param db_type: Database type like PostgreSQL, MySQL, etc..
        param db_url: Database URL
        param tar_loc: Target location to dump the files
        param file_extn: File extension like .sql, .txt
        param incl_db_objs: Database objects
    Returns:
        None:
    Raises:
        Raise an error if schema generator fails
    """
    try:
        logger.info("Starts the schema generator")
        if db_type == "sqlite":
            logger.info("Starts the SQLite DB schema generator")
            dump_sqlite.main(db_url, tar_loc, file_extn, incl_db_objs)
    except Exception as msg:
        logger.error("Schema generator failed")
        raise Exception(msg)
