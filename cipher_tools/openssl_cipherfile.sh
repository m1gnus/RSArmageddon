#!/bin/env bash

if [[ $1 == 'encrypt' ]]
then
    openssl rsautl -encrypt -in $2 -out $3 -pubin -inkey $4
fi

if [[ $1 == 'decrypt' ]]
then
    openssl rsautl -decrypt -in $2 -out $3 -inkey $4
fi
