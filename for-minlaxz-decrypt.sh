#! /bin/bash

HEAD='\e[7;36m'
RESET='\e[m'
OUTPUT='\e[32m'
NL='\n'
ERROR='\e[3;31m'
WARN='\e[3;33m'

function oneLineOutput() {
    line=$1
    echo -e "${OUTPUT}$line${RESET}"
}

function descriptionOutput() {
    line=$1
    echo -e "${WARN}Description : $line ${RESET}"
}

function warningOutput() {
    line=$1
    echo -e "${ERROR}Warning : $line ${RESET}"
}

oneLineOutput "decrypting telegram credentials."
openssl enc -aes-256-cbc -d -salt -pbkdf2 -in telegram.encrypted -out telegram_secs.py
oneLineOutput "decrypting twitter credentials."
openssl enc -aes-256-cbc -d -salt -pbkdf2 -in twitter.encrypted -out twitter_secs.py
descriptionOutput "decrypting telegram sessions."
openssl enc -aes-256-cbc -d -salt -pbkdf2 -in anone.encrypted -out anon.session
warningOutput "Done, run tele-tweet with 'python main.py'"
