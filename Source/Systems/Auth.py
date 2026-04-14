from ctypes import CDLL, c_int, c_char_p
import json
import os
import sys

# ====== runtime guard ======
LIB_PATH = os.path.join("/opt/Innovations/System", "libanv_core.so")
lib = CDLL(LIB_PATH)
lib.anv_is_allowed_runtime.restype = c_int
lib.anv_get_last_reason.restype = c_char_p
lib.anv_get_last_details_json.restype = c_char_p


def authorize_environment():
    allowed = bool(lib.anv_is_allowed_runtime())
    reason = lib.anv_get_last_reason().decode("utf-8", errors="replace")

    if not allowed:
        return 0, reason
    else:
        return 1, None

# ====== アプリ本体 ======
def run_app():
    print("アプリ本体スタート")
    # ここに既存処理


# ====== エントリーポイント ======
def main():
    try:
        authorize_environment()
        print(authorize_environment())
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
    input(" >> ")