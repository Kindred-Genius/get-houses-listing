#!/bin/bash

conda activate gethouses
export PATH="$PATH:/home/ubuntu/firefoxdriver"
cd project/get-houses-listing/
python src/main.py