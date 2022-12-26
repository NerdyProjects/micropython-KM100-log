#!/bin/sh
while [ true ]; do
  /usr/bin/micropython `pwd`/run.py
  sleep 5
done

