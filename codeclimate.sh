#!/bin/bash

if [[ "${TRAVIS_BRANCH}" = "master" && "${PY_VER}" = "2.7.10" ]]; then
  git checkout master
  curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
  chmod +x ./cc-test-reporter
  ./cc-test-reporter before-build
  /opt/python/bin/python -mpy.test --cov=cloudpassage tests
  ./cc-test-reporter after-build --exit-code ${TRAVIS_TEST_RESULT}
fi
