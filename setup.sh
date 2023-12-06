#!/bin/bash

git config --system core.longpaths true
git config --global core.longpaths true

cp ".env copy" ".env"

pip install -r requirements.lib

echo "Setup successfully!"

sleep 5