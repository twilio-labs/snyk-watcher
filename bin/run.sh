#!/usr/bin/env bash

gunicorn app.main:app -b 0.0.0.0:8000 -w 3 -k uvicorn.workers.UvicornWorker
