#!/usr/bin/env bash

dtstamp=$(date +%Y%m%d_%H%M%S)
. ~/.virtualenvs/garage_sales/bin/activate

git pull
./update.py
git add -A
git commit -m "$dtstamp"
git push

deactivate