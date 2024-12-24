#!/bin/bash

if [[ "$@" == "" ]]; then
    echo "Usage: $0 domains_1.txt [domains_N.txt]"
    exit 1
fi

http_prob() {
    result="$(curl -I $1 2>/dev/null)"
    status=$(echo $result | cut -d' ' -f2)

    if [ $(echo $status | grep -E '[0-9]{3}') ]; then
        echo "$status:$domain"
    fi

    exit 0
}

for file in "$@"; do
    if ! test -f $file; then
        echo "Error: '$file' - Is not a File"
        exit 1
    else 
        for domain in $(cat $file); do
            http_prob $domain &
        done
    fi 
done

