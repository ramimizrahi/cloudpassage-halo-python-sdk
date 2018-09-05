#!/bin/bash
if [ "$TRAVIS_BRANCH" == "master" ]; then
   docker run -it --rm -e HALO_API_KEY=$HALO_API_KEY -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY -e HALO_API_HOSTNAME=$HALO_API_HOSTNAME -e HALO_API_PORT=$HALO_API_PORT -e CODECLIMATE_REPO_TOKEN=$CODECLIMATE_REPO_TOKEN cloudpassage_halo_python_sdk /bin/sh -c "py.test tests";
else
   docker run -it --rm -e HALO_API_KEY=$HALO_API_KEY -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY -e HALO_API_HOSTNAME=$HALO_API_HOSTNAME -e HALO_API_PORT=$HALO_API_PORT cloudpassage_halo_python_sdk /bin/sh -c "py.test --profile tests/";

fi
