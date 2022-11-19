#!/bin/bash
jsonString='{"results":[{ "uri": "test"} ]}'
#jsonString='{"results":[ ]}'
echo $jsonString


echo $jsonString | jq '.results[0].uri'


count=$(echo $jsonString | jq '.results[] | length')
echo "count $count"

if [[ $count == 1 ]]; then
   echo "objects there"
else
   echo "object not there"   
fi
