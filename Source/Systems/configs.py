import configparser
import os

def load_weekconfigs():
    if os.path.exists('/etc/AutoTrade/config.ini'):
        # ConfigParser オブジェクトを作成
        config = configparser.ConfigParser()

        # ファイルを読み込む
        config.read('/etc/AutoTrade/config.ini')

        # 値を取得
        host = config.get('settings', 'value')
        return int(host)
    else:
        return 0
