#!/bin/bash
WORKING_DIR=/var/www/desklib
cd ${WORKING_DIR}
source .dev.envrc
source ../venv/bin/activate
exec $@

