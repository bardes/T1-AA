#!/bin/bash

RUNS=$1
FILES=$(find . -maxdepth 1 -regextype posix-extended -regex '^.*\.in$')
PROG='../color.py'

for IN_FILE in $FILES
do
    for l in a b c d
    do
        echo ",$l" > $IN_FILE.$l
        tail -n +2 $IN_FILE >> $IN_FILE.$l
    done
done


printf "#FILE_NAME\tAVG_ATTRS\tSD_ATTRS\tAVG_TIME\tSD_TIME\n" > results

for IN_FILE in $(ls *.in.[abcd])
do
    printf "Calculating \"$IN_FILE\"\t"
    truncate -s0 .tmp_attrs .tmp_times
    
    for ((n=0; n<$RUNS; n++))
    do
        /usr/bin/time -f '%e' $PROG -s -a $IN_FILE 2>> .tmp_times | cut -f2 >> .tmp_attrs
        printf "#"
    done
    echo

    printf "$IN_FILE\t" >> results
    awk '{s+=$1}END{printf "%f\t", s/NR}' .tmp_attrs >> results
    awk '{sum+=$1; sumsq+=$1*$1}END{printf "%f\t", sqrt(sumsq/NR - (sum/NR)**2)}' .tmp_attrs >> results
    awk '{s+=$1}END{printf "%f\t", s/NR}' .tmp_times >> results
    awk '{sum+=$1; sumsq+=$1*$1}END{printf "%f\t", sqrt(sumsq/NR - (sum/NR)**2)}' .tmp_times >> results
    echo >> results
done

rm -f .tmp_attrs .tmp_times
rm -r *.in.[abcd]
