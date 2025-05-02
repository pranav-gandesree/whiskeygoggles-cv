#!/bin/bash
gunicorn app:app --chdir web --bind 0.0.0.0:$PORT
