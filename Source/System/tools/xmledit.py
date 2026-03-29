import sys
import xml.etree.ElementTree as ET
import subprocess

XML_PATH = "bot_config.xml"


def load_xml():
    try:
        return ET.parse(XML_PATH)
    except FileNotFoundError:
        print("❌ bot_config.xml が見つかりません")
        sys.exit(1)

def ask_restart():
    try:
        ans = input("🔁 サービスを再起動しますか？ [y/N]: ").strip().lower()
        if ans in ("y", "yes"):
            print("▶ 再起動スクリプトを実行します...")
            subprocess.run(
                ["/opt/Innovation/System/tools/Restart.sh"],
                check=True
            )
            print("✅ 再起動完了")
        else:
            print("ℹ 再起動はスキップしました")
    except subprocess.CalledProcessError:
        print("❌ 再起動スクリプトの実行に失敗しました")
    except KeyboardInterrupt:
        print("\n⏹ 中断されました")

def view_configs(tree):
    root = tree.getroot()

    rows = []
    max_key_len = 0
    max_val_len = 0

    # まず全データ収集
    for table in root.findall(".//table"):
        key = table.find("./column[@name='key']")
        value = table.find("./column[@name='value']")
        ettc = table.find("./column[@name='ettc']")

        if key is not None and value is not None:
            k = key.text or ""
            v = value.text or ""
            d = ettc.text if ettc is not None else ""

            rows.append((k, v, d))
            max_key_len = max(max_key_len, len(k))
            max_val_len = max(max_val_len, len(v))
    print(" ")
    # ヘッダ
    print(
        f"{'KEY'.ljust(max_key_len)}  "
        f"{'VALUE'.ljust(max_val_len)}  "
        f"DESCRIPTION"
    )
    print("-" * (max_key_len + max_val_len + 15))

    # 本体
    for k, v, d in rows:
        print(
            f"{k.ljust(max_key_len)}  "
            f"{v.ljust(max_val_len)}  "
            f"{d}"
        )


def update_config(tree, target_key, new_value):
    root = tree.getroot()

    for table in root.findall(".//table"):
        key = table.find("./column[@name='key']")
        value = table.find("./column[@name='value']")

        if key is not None and key.text == target_key:
            old = value.text
            value.text = str(new_value)
            print(f"✅ {target_key}: {old} → {new_value}")
            return True

    print(f"❌ key '{target_key}' が見つかりません")
    return False


def main():
    if len(sys.argv) < 2:
        print("使い方:")
        print("  python xedit.py view")
        print("  python xedit.py [KEY] [VALUE]")
        sys.exit(0)

    tree = load_xml()

    if sys.argv[1] == "view":
        view_configs(tree)
        return

    if len(sys.argv) != 3:
        print("❌ 引数が不正です")
        sys.exit(1)

    key = sys.argv[1]
    value = sys.argv[2]

    if update_config(tree, key, value):
        tree.write(XML_PATH, encoding="utf-8", xml_declaration=True)
        ask_restart()

if __name__ == "__main__":
    main()
