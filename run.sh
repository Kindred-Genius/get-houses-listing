#!/bin/bash

source /home/ubuntu/miniconda3/bin/activate gethouses
export PATH="$PATH:/home/ubuntu/firefoxdriver"
cd project/get-houses-listing/
python src/main.py