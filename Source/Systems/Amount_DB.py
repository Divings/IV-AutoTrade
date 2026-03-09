import mysql.connector
from decimal import Decimal
from datetime import date, timedelta
from typing import Optional
import os
import sqlite3
from decimal import Decimal
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

DB_PATH = Path("/var/lib/AutoTrade/trade_log.db")


def _ensure_db_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def _get_conn() -> sqlite3.Connection:
    _ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_realized_pnl (
            trade_date TEXT PRIMARY KEY,
            pnl TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def _to_decimal(v) -> Decimal:
    if v is None:
        return Decimal("0")
    if isinstance(v, Decimal):
        return v
    return Decimal(str(v))

def upsert_daily_pnl(trade_date: date, pnl) -> None:
    """1日1行で当日決算損益を保存（同日があれば上書き）"""
    pnl = _to_decimal(pnl)

    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT OR REPLACE INTO daily_realized_pnl (trade_date, pnl)
            VALUES (?, ?)
            """,
            (trade_date.isoformat(), str(pnl))
        )
        conn.commit()
    finally:
        conn.close()

def get_daily_pnl(trade_date: date) -> Optional[Decimal]:
    """指定日の当日決算損益をDecimalで返す。無ければNone。"""
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT pnl FROM daily_realized_pnl WHERE trade_date = ?",
            (trade_date.isoformat(),)
        )
        row = cur.fetchone()
        return Decimal(str(row[0])) if row else None
    finally:
        conn.close()

def get_today_pnl(default: Optional[Decimal] = None) -> Optional[Decimal]:
    """今日の損益。無ければdefault（未指定ならNone）。"""
    v = get_daily_pnl(date.today())
    return v if v is not None else default


def get_yesterday_pnl(default: Optional[Decimal] = None) -> Optional[Decimal]:
    """前日の損益。無ければdefault（未指定ならNone）。"""
    v = get_daily_pnl(date.today() - timedelta(days=1))
    return v if v is not None else default

if __name__ == "__main__":
    upsert_daily_pnl(date.today(), "-1234.56")
    print("today:", get_today_pnl(default=Decimal("0")))
    print("yesterday:", get_yesterday_pnl(default=Decimal("0")))