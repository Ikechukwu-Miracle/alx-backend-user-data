#!/usr/bin/env python3
"""Filtered logger"""
import logging
import re
from typing import List
import os
from mysql.connector import connection


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                      field + "=" + redaction + separator, message)
    
    return message


def get_logger() -> logging.Logger:
    """Returns a logger object"""
    logger = logging.get_logger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.streamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to the database
    (mysql.connector.connection.MySQLConnection object).
    """
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.environ.get("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.MySQLConnection(
        user=username,
        password=password,
        host=host,
        database=database
    )

    return db


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters incoming log records"""
        message = filter_datum(
            self.fields, self.REDACTION, super(
                RedactingFormatter, self).format(record),
            self.SEPARATOR)
        
        return message


def main():
    """Main function of filtered logger module"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fetch = cursor.fetchall()

    logger = get_logger()

    for row in fetch:
        fields = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; '\
            'last_login={}; user_agent={};'
        fields = fields.format(row[0], row[1], row[2], row[3],
                               row[4], row[5], row[6], row[7])
        logger.info(fields)
    
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
