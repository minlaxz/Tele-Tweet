#! /bin/bash
openssl enc -aes-256-cbc -d -salt -pbkdf2 -in telegram.encrypted -out telegram_secs.py
openssl enc -aes-256-cbc -d -salt -pbkdf2 -in twitter.encrypted -out twitter_secs.py
