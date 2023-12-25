#!/bin/bash

sleep 15

celery -A config.celery worker -l INFO -S django