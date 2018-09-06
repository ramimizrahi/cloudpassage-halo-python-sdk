#!/bin/bash
docker run \
    -it \
    --rm \
    -e HALO_API_KEY=$HALO_API_KEY \
    -e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
    -e HALO_API_HOSTNAME=$HALO_API_HOSTNAME \
    -e HALO_API_PORT=$HALO_API_PORT \
    cloudpassage_halo_python_sdk /bin/sh -c "/opt/python/bin/python -mpy.test --cov=cloudpassage --cov-report term --profile tests/"
