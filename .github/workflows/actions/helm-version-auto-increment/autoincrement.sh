#!/bin/bash

# input validation
if [[ -z "${HELM_VERSION}" ]]; then
   echo "No tag name supplied"
   exit 1
fi

if [[ -z "${CHART_PATH}" ]]; then
   echo "No tag name supplied"
   exit 1
fi

echo "inputs: helm version: ${HELM_VERSION}, chart_path:  ${CHART_PATH}"

tag=$(git describe --tags --abbrev=0)
echo "tag : $tag"


git diff --quiet HEAD ${tag} -- ${CHART_PATH}
cf=$?
echo "cf: $cf"

if [[ $cf != 0 ]]; then
   echo "There is a change in helm chart"
else 
  echo "There is no change in helm chart"
fi

                  
                  
