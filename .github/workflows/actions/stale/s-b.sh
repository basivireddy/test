#!/bin/bash
#set -x

cutoffInterval="-2 day"
cutoffDate=`date -I --date="${cutoffInterval}"`

function usage {
    echo "$0:"
    echo "sh script.sh git-repo-directory"
}

if [ "$1" == "" ]; then
    usage
    exit 1
fi

root="$1"

if [ ! -d "${root}/.git" ]; then
   usage
   echo "Erro: No .git repo found at ${root}"
   exit 1
fi
OLD=`pwd`
cd $root

echo "below branches have last commit before ${cutoffDate} date"
git branch --no-abbrev -a | sed 's/\*//' | sed 's/->//' | sed 's/ //' | grep -v '/HEAD' | while read br; do
    git log --date=iso -n 1 "$br" >/tmp/$$.gc2 2>/dev/null
    dayte=`head -3 /tmp/$$.gc2 | tail -1 | awk '{ print $2}'`
    auth=`head -2 /tmp/$$.gc2 | tail -1 | awk '{ $1=""; print $0; }'`

    if [[ "$dayte" < "$cutoffDate" ]]; then
      echo "${dayte} ${br} ${auth}"
      if [[ ! "${dayte}" =~ [0-9]+ ]]; then
        echo
        cat /tmp/$$.gc2
        echo
        echo

      fi
    fi
done

rm /tmp/$$.gc2

cd $OLD


