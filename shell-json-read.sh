#!/bin/bash
jsonString='{"results":[{ "uri": "test"}, { "uri": "test"} ]}'
#jsonString='{"results":[ ]}'
echo $jsonString


echo $jsonString | jq '.results[0].uri'


count=$(echo $jsonString | jq '.results[] | length')
echo "count $count"

if [[ $count == 0 ]]; then
   echo "objects not there"
else
   echo "object  there"   
fi
