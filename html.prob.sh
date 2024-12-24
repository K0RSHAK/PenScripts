#!/bin/bash

pattern=
out=hp.out.txt
counter=0
lines=0

if ! test -f "$1"; then 
    pattern=$1
    shift
fi

if [[ "$@" == "" ]]; then
    echo "Usage: $0 domains_1.txt [domains_N.txt]"
    exit 1
fi

echo
echo "Searching in domains for '$pattern'"

http_prob() {
    result_1="$(curl -L "https://$1" 2>/dev/null)"
    result_2="$(curl -L "http://$1" 2>/dev/null)"

    if [[ "$(echo $result_1 | grep $pattern)" != "" ]] || [[ "$(echo $result_2 | grep $pattern)" != "" ]]; then
        echo "$1" >> $out
    fi

    # exit 0
}

for file in "$@"; do
    l=$(wc -l $file | cut -d' ' -f 6)
    lines=$(($lines+$l))
done

for file in "$@"; do
    if ! test -f $file; then
        echo "Error: '$file' - Is not a File"
        exit 1
    else 
        for domain in $(cat $file); do
            http_prob $domain
            counter=$(($counter+1))
            printf "\rProgress: $counter/$lines"
        done
    fi
    echo
    echo "Result will be sent to the $out"
    echo 
done