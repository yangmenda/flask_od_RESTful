#!/bin/bash
gunicorn server:app -c gunicorn.conf.py --timeout 36000
