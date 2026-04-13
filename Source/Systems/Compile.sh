#!/usr/bin/bash
cd ./
pyinstaller AutoTrade.spec
sudo cp dist/AutoTrade /mnt/data/IV-AutoTrade/Source/System