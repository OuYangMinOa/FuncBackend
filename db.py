"""資料庫連線與表名設定。"""
import os

import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_TABLE = os.getenv("DB_TABLE", "FUNC_TABLE")

_CONN_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}


def get_conn():
    """每次取得一條新的連線。"""
    return pymysql.connect(**_CONN_CONFIG)
