#! /usr/bin/env bash

if [ "$1" = "worker" ]; then
  echo "Migrating backend..."
  cd icon_contracts
  alembic upgrade head
  echo "Starting worker..."
  python main_worker.py

elif [ "$1" = "api" ]; then
  echo "Starting API..."
  python icon_contracts/main_api.py
else
  echo "No args specified - exiting..."
fi
