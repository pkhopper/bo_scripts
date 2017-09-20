#!/bin/bash
nohup python manage.py runserver 0.0.0.0:1237 --noreload > log.txt 2>&1 &