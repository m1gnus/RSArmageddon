#!/bin/env bash

# OpenSSL Wrapper -- https://www.openssl.org/

# $1 operating mode
# $2 input_file
# $3 output_file
# $4 path to key
# $5 padding type

if [[ $1 == 'encrypt' ]]
then
    openssl rsautl -encrypt -"$5" -in "$2" -out "$3" -pubin -inkey "$4"
fi

if [[ $1 == 'decrypt' ]]
then
    openssl rsautl -decrypt -"$5" -in "$2" -out "$3" -inkey "$4"
fi
