#!/usr/bin/env bash

source venv/bin/activate
celery -A workers.celery_app worker --beat -l info
