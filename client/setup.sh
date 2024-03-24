#!/bin/bash
sudo apt update && sudo apt upgrade --yes
sudo apt install python3
sudo apt install python3-pip
pip install -r ./requirements.txt