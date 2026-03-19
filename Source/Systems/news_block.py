import csv
from datetime import datetime, timedelta, time
import os
#CSV_PATH = "news.csv"

# 指標前後のブロック幅（分）


def load_conf_BEFORE():
    import configparser
    
    # 設定ファイル読み込み
    config = configparser.ConfigParser()
    config.read("/etc/AutoTrade/config.ini", encoding="utf-8")
    BLOCK_BEFORE_MIN  = config.getint("NEWSBLOCK", "BLOCK_BEFORE_MIN", fallback=30)# デフォルトは有効(1)
    return BLOCK_BEFORE_MIN

def load_conf_AFTER():
    import configparser
    
    # 設定ファイル読み込み
    config = configparser.ConfigParser()
    config.read("/etc/AutoTrade/config.ini", encoding="utf-8")
    BLOCK_AFTER_MIN  = config.getint("NEWSBLOCK", "BLOCK_AFTER_MIN", fallback=20)# デフォルトは有効(1)
    return BLOCK_AFTER_MIN


BLOCK_AFTER_MIN = load_conf_AFTER()
BLOCK_BEFORE_MIN = load_conf_BEFORE()

def write_log(CSV_PATH):
    path="/var/log/AutoTrade/news_block_log.txt"
    with open(path, "a") as f:
        f.write(f"{datetime.now().isoformat()}\n")
        f.write(f"CSV_PATH: {CSV_PATH}\n")
        f.write(f"Exists: {os.path.exists(CSV_PATH)}\n")
        f.write("\n")
    return 0

def init(path):
    from pathlib import Path
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def get_block_minutes(importance: int) -> int:
    """
    指標重要度に応じたブロック時間（分）を返す
    """
    if importance >= 3:
        return BLOCK_BEFORE_MIN
    return BLOCK_AFTER_MIN

from datetime import datetime

def get_weekly_news_path(base_dir="datas"):
    now = datetime.now()
    week = now.isocalendar().week
    return init(base_dir) / f"news-w{week}.csv"

CSV_PATH = get_weekly_news_path()
write_log(CSV_PATH)

# ニュース指標のブロック時間を読み込む
def load_news_blocks(target_date: datetime.date):
    blocks = []

    if not os.path.exists(CSV_PATH):
        return blocks

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["date"] != target_date.isoformat():
                continue

            hh, mm = map(int, row["time"].split(":"))
            event_dt = datetime.combine(target_date, time(hh, mm))

            importance = int(row["importance"])
            block_min = get_block_minutes(importance)

            start = event_dt - timedelta(minutes=block_min)
            end = event_dt + timedelta(minutes=block_min)

            blocks.append((
                start,
                end,
                row["currency"],
                importance
            ))

    return blocks

def is_blocked(now: datetime, blocks):
    for start, end, currency, importance in blocks:
        if start <= now <= end:
            return True, start, end, currency, importance
    return False, None, None, None, None
