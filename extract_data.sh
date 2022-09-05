#!/bin/bash
# script to extract validation results from each data folder

shopt -s nullglob

output=result
fileName=batch_validation_results.txt

find . -name $fileName -print0 | xargs -0 -I '{}' bash -c "mkdir -p $output/\`dirname '{}'\` && cp '{}' $output/'{}'"
