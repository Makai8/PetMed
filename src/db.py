"""Database access. Every query in the app goes through query() and query_one().

Write SQL with %s placeholders, exactly as mysql-connector expects.
"""
from flask import g

import config


def _connect():
    if config.DB_ENGINE == "sqlite":
        import sqlite3

        conn = sqlite3.connect(config.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    import mysql.connector

    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
    )


def get_db():
    """One connection per request, closed automatically afterward."""
    if "db" not in g:
        g.db = _connect()
    return g.db


def close_db(_error=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def query(sql, params=()):
    """Run a SELECT and return a list of dicts (column name -> value)."""
    conn = get_db()
    if config.DB_ENGINE == "sqlite":
        cur = conn.execute(sql.replace("%s", "?"), tuple(params))
        rows = [dict(r) for r in cur.fetchall()]
        cur.close()
        return rows

    cur = conn.cursor(dictionary=True)
    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    cur.close()
    return rows


def query_one(sql, params=()):
    rows = query(sql, params)
    return rows[0] if rows else None
