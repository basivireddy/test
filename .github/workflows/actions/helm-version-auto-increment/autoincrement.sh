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


tag=$(git describe --tags --abbrev=0 HEAD --always)
echo "tag : $tag"


cf=$(git diff --quiet HEAD ${tag} -- ${CHART_PATH})

echo "${cf}"

if ( cf != 0 ) {
                     echo "There is a change in helm chart"
#                     Updated_HELM_VERSION = sh (script: "echo ${HELM_VERSION} | awk -F. '{\$NF = \$NF + 1;} 1' | sed 's/ /./g'", returnStdout: true).trim()
#                     echo "${Updated_HELM_VERSION}"
}
else {
  echo "There is no change in helm chart"
  
}

                  
                  
