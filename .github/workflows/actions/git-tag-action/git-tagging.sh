#!/bin/bash
set -x

# input validation
if [[ -z "${TAG}" ]]; then
   echo "No tag name supplied"
   exit 1
fi

if [[ -z "${GITHUB_TOKEN}" ]]; then
   echo "No github token supplied"
   exit 1
fi

# check if tag already exists
tag_exists="false"
if [ $(git tag -l "$TAG") ]; then
    tag_exists="true"
fi
jshon -e foo -u <<< '{ "foo":"bar" }' 
jq -V
echo "jq version"

echo "$GITHUB_EVENT_PATH"
cat "$GITHUB_EVENT_PATH"


# push the tag to github
git_refs_url=$(jq .repository.git_refs_url $GITHUB_EVENT_PATH | tr -d '"' | sed 's/{\/sha}//g')

echo "**pushing tag $TAG to repo $GITHUB_REPOSITORY"

if $tag_exists
then
  # update tag
  curl -s -k -X PATCH "$git_refs_url/tags/$TAG" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d @- << EOF

  {
    "sha": "$GITHUB_SHA",
    "force": true
  }
EOF
else
  # create new tag
  curl -s -k -X POST $git_refs_url \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d @- << EOF

  {
    "ref": "refs/tags/$TAG",
    "sha": "$GITHUB_SHA"
  }
EOF
fi
