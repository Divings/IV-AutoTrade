import os
import re
from datetime import datetime, timedelta

def get_fx_debug_log(
    target_filename="/var/log/AutoTrade/fx_debug_log.txt"
):
    try:
        log_path = target_filename

        if not os.path.isfile(log_path):
            print(f"[エラー] ログファイルが見つかりません: {log_path}")
            return

        print(f"[情報] ログファイル: {log_path}")

        now = datetime.now()
        cutoff = now - timedelta(hours=1)

        with open(log_path, "r") as log_file:
            for line in log_file:
                # 例: 2026-01-14 12:34:56
                m = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', line)
                if not m:
                    continue

                log_time = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
                if log_time >= cutoff:
                    print(line, end="")

    except Exception as e:
        print(f"[例外エラー] {e}")

# 実行
get_fx_debug_log()

