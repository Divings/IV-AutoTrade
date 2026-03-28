#!/bin/bash

# 対象ディレクトリ
TARGET_DIRS=(
    "/etc/AutoTrade"
    "/var/log/AutoTrade"
)

# 所有者
OWNER="autotrade:autotrade"

for DIR in "${TARGET_DIRS[@]}"; do
    if [ -d "$DIR" ]; then
        echo "Processing $DIR ..."
        chown -R $OWNER "$DIR"
    else
        echo "Directory not found: $DIR"
    fi
done

echo "Done."