#!/bin/bash

if [[ "$@" == "" ]]; then
    echo "Usage: $0 domains_1.txt [domains_N.txt]"
    exit 1
fi

domain_check() {
    if [ "$(ping -c 2 $1 2>/dev/null | grep -E '[12] packets received')" != "" ]; then
        echo $1
    fi
    exit 0
}

for file in "$@"; do
    if ! test -f $file; then
        echo "Error: '$file' - Is not a File"
        exit 1
    else 
        for domain in $(cat $file); do
            domain_check $domain &
        done
    fi 
done

