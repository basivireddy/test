#!/bin/bash

# Input Validation
if [[ -z "${CHART_PATH}" ]]; then
   echo "No tag name supplied"
   exit 1
fi

# Helm Version
grep "version:" ./$CHART_PATH/Chart.yaml
HELM_version=$(grep "version:" ./$CHART_PATH/Chart.yaml | awk '{print $2}')
echo "HELM_version : $HELM_version"


echo "inputs: helm version: ${HELM_VERSION}, chart_path:  ${CHART_PATH}"

tag=$(git describe --tags --abbrev=0 HEAD)
echo "tag : $tag"


git diff --quiet HEAD ${tag} -- ${CHART_PATH}
cf=$?
echo "cf: $cf"

if [[ $cf != 0 ]]; then
   echo "There is a change in helm chart"
else 
  echo "There is no change in helm chart"
fi

                  
                  
