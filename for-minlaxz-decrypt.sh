#! /bin/bash

openssl enc -aes-256-cbc -d -salt -pbkdf2 -in ./credentials.encrypted -out ./credentials.py
