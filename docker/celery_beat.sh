#!/bin/bash

sleep 15

celery -A config beat -l INFO -S django