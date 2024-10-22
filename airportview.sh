#!/bin/bash

for url in "airside-operations" "passenger-experience" "atcatm" "construction-design" "regulation-legislation" "revenues" "terminal-operations"
do
    docker run -v $(pwd)/data:/app/data airport_crawler -u ${url} -s csv
done
