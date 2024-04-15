#!/bin/bash

alembic upgrade head

python3 src/api.py & echo $! >> ../balancer_pids.txt

while true; do sleep 1000; done