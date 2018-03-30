#!/bin/bash

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
  git checkout $TRAVIS_BRANCH
  git pull
}

setup_git

bumpversion --no-tag --message '[ci skip] Travis bump version: {current_version} → {new_version}' patch

git push --tags "https://${GH_TOKEN}@github.com/buluba89/Yatcobot.git" $TRAVIS_BRANCH

curl -H "Content-Type: application/json" --data '{"source_type": "$TRAVIS_BRANCH", "source_name": "staging"}' -X POST https://registry.hub.docker.com/u/buluba89/yatcobot/trigger/$DH_TOKEN/