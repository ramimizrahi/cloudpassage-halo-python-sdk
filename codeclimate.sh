#!/bin/bash

if [ "${PY_VER}" = "2.7.10" ]; then
  apt-get update && apt-get install -y git
  curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
  chmod +x ./cc-test-reporter
  ./cc-test-reporter before-build
  /opt/python/bin/python -mpy.test --cov-report xml --cov=cloudpassage tests
  export TEST_STATUS=$?
  ./cc-test-reporter after-build --exit-code ${TEST_STATUS}
else
  /opt/python/bin/python -mpy.test --cov=cloudpassage --cov-report term-missing --profile tests/
  export TEST_STATUS=$?
fi

exit ${TEST_STATUS}
