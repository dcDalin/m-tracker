"""
Main CLI App
"""
import sys

import click
import psycopg2
from psycopg2 import connect

from api.server import APP


# Common variables
MAIN_DB = APP.config.get('DATABASE_NAME')
TEST_DB = APP.config.get('DATABASE_NAME') + "_test"
DEFAULT_DB = "postgres"
INITIAL_CONNECT = {
    "host": APP.config.get('DATABASE_HOST'),
    "database": DEFAULT_DB,
    "user": APP.config.get('DATABASE_USER'),
    "password": APP.config.get('DATABASE_PASS')
}
DB_CONNECT = {
    "host": APP.config.get('DATABASE_HOST'),
    "database": MAIN_DB,
    "user": APP.config.get('DATABASE_USER'),
    "password": APP.config.get('DATABASE_PASS')
}
TEST_DB_CONNECT = {
    "host": APP.config.get('DATABASE_HOST'),
    "database": TEST_DB,
    "user": APP.config.get('DATABASE_USER'),
    "password": APP.config.get('DATABASE_PASS')
}


@click.group()
@click.version_option()
def cli():
    """
    ✨✨✨✨ M-Tracker CLI ✨✨✨✨
    """


@cli.group()
def create():
    """Database related create Functions."""


@create.command('db')
def create_db():
    """Creates a new database."""
    # drop then create the main and test db
    drop_statement = "DROP DATABASE IF EXISTS {};".format(MAIN_DB)
    test_drop_statement = "DROP DATABASE IF EXISTS {};".format(TEST_DB)
    ddl_statement = "CREATE DATABASE {};".format(MAIN_DB)
    test_ddl_statement = "CREATE DATABASE {};".format(TEST_DB)
    conn = connect(**INITIAL_CONNECT)
    conn.autocommit = True

    try:
        with conn.cursor() as cursor:
            # execute ddls
            cursor.execute(drop_statement)
            cursor.execute(test_drop_statement)
            cursor.execute(ddl_statement)
            cursor.execute(test_ddl_statement)
        conn.close()
        click.secho('  SUCCESS!  ', bg='green', fg='white', bold=True)
        click.secho("Created database environment successfully created",
                    bg='white', fg='black', bold=True)
    except psycopg2.Error:
        click.secho('  ERROR!  ', bg='red', fg='white', bold=True)
        raise SystemExit(
            "Failed to setup Postgres environment.\n{0}".format(sys.exc_info())
        )


@create.command('schema')
def create_schema():
    """Creates SQL Schema."""
    # Populate Main DB
    try:
        main_conn = connect(**DB_CONNECT)
        main_conn.autocommit = True
        with main_conn.cursor() as cursor:
            cursor.execute(open("schema.sql", "r").read())
        main_conn.close()
        click.secho('  SUCCESS!  ', bg='green', fg='white', bold=True)
        click.secho("Schema populated successfully",
                    bg='white', fg='black', bold=True)
    except psycopg2.Error:
        click.secho('  SORRY!  ', bg='red', fg='white', bold=True)
        raise SystemExit(
            "Failed to load schema.\n{0}".format(sys.exc_info())
        )


@create.command('test-schema')
def create_test_schema():
    """Creates SQL Schema for Test DB."""
    # Populate Test Main DB
    try:
        test_conn = connect(**TEST_DB_CONNECT)
        test_conn.autocommit = True
        with test_conn.cursor() as cursor:
            cursor.execute(open("schema.sql", "r").read())
        test_conn.close()
        click.secho('  SUCCESS!  ', bg='green', fg='white', bold=True)
        click.secho("Test Schema populated successfully",
                    bg='white', fg='black', bold=True)
    except psycopg2.Error:
        click.secho('  SORRY!  ', bg='red', fg='white', bold=True)
        raise SystemExit(
            "Failed to load test schema.\n{0}".format(sys.exc_info())
        )