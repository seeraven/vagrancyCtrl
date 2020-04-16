#!/bin/bash -eu
# ----------------------------------------------------------------------------
# Functional tests for the vagrancyCtrl command
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
#  SETTINGS
# ----------------------------------------------------------------------------

export TEST_BASE_DIR=$(dirname $(readlink -f $0))
BASE_DIR=$(dirname $(dirname $TEST_BASE_DIR))
VAGRANCYCTRL_BIN=${BASE_DIR}/vagrancyCtrl


# -----------------------------------------------------------------------------
# CHECK COMMAND LINE ARGUMENTS
# -----------------------------------------------------------------------------
VAGRANCY_IMAGE=seeraven/vagrancy:0.0.5
SAVE_REFERENCE=0
VERBOSE=0
WAIT_ON_ERROR=0

function usage() {
    echo
    echo "Usage: $1 [-h] [-d <docker image>] [-s] [-c|-p] [-v] [-w]"
    echo ""
    echo "Functional tests of vagrancyCtrl using a docker containerized vagrancy."
    echo
    echo "Options:"
    echo " -h                : Print this help."
    echo " -d <docker image> : The docker image to use (default: ${VAGRANCY_IMAGE})."
    echo " -s                : Save the vagrancyCtrl output as reference."
    echo " -c                : Use the coverage wrapper."
    echo " -p                : Use the pyinstaller generated executable."
    echo " -v                : Be more verbose."
    echo " -w                : Wait before stopping the docker container when a test failed."
    exit 1
}

while getopts ":hd:scpvw" OPT; do
    case $OPT in
	h )
	    usage $0
	    ;;
	d )
	    VAGRANCY_IMAGE=$OPTARG
	    ;;
	s )
	    SAVE_REFERENCE=1
	    ;;
	c )
	    VAGRANCYCTRL_BIN="coverage run --append --rcfile=${BASE_DIR}/.coveragerc-functional $VAGRANCYCTRL_BIN"
	    ;;
	p )
	    VAGRANCYCTRL_BIN=${BASE_DIR}/dist/vagrancyCtrl
	    ;;
	v )
	    VERBOSE=1
	    ;;
	w )
	    WAIT_ON_ERROR=1
	    ;;
	\? )
	    usage $0
	    ;;
    esac
done


# -----------------------------------------------------------------------------
# EXPORTS FOR TEST SCRIPTS
# -----------------------------------------------------------------------------
export EXPECTED_OUTPUT_DIR=$TEST_BASE_DIR/expected
mkdir -p ${EXPECTED_OUTPUT_DIR}
export VAGRANCYCTRL_BIN
export SAVE_REFERENCE
export VAGRANCY_DATA_DIR=/tmp/vagrancy_test


# -----------------------------------------------------------------------------
# START VAGRANCY
# -----------------------------------------------------------------------------
echo "Starting vagrancy image ${VAGRANCY_IMAGE}..."
rm -rf   ${VAGRANCY_DATA_DIR}
mkdir -p ${VAGRANCY_DATA_DIR}
docker run --rm -d \
       --name vagrancy_test \
       -v ${VAGRANCY_DATA_DIR}:/data \
       -p 127.0.0.1:9000:9000 \
       ${VAGRANCY_IMAGE} -p 9000
sleep 5s
echo "Vagrancy started at http://127.0.0.1:9000"
export VAGRANCY_URL=http://127.0.0.1:9000


# -----------------------------------------------------------------------------
# RUN TESTS
# -----------------------------------------------------------------------------
RETVAL=0
TMPOUTPUT=$(tempfile)

for SCRIPT in ${TEST_BASE_DIR}/tests/*.sh; do
    echo -n "Running test $(basename $SCRIPT) ... "
    if $SCRIPT &> $TMPOUTPUT; then
	echo "OK"
	if [[ $VERBOSE -eq 1 ]]; then
	    echo "-----------------------------------------------------------------"
	    echo " Output:"
	    cat $TMPOUTPUT
	    echo "-----------------------------------------------------------------"
	fi
    else
	echo "FAILED"
	echo "-----------------------------------------------------------------"
	echo " Output:"
	cat $TMPOUTPUT
	echo "-----------------------------------------------------------------"
	echo " Vagrancy Log:"
	docker logs vagrancy_test
	echo "-----------------------------------------------------------------"
	RETVAL=1
    fi
done

rm -f $TMPOUTPUT

if [ $WAIT_ON_ERROR -eq 1 -a $RETVAL -eq 1 ]; then
    echo "Requested wait on error. Press any key to continue..."
    read -n 1
    echo "Continuing..."
fi

# -----------------------------------------------------------------------------
# STOP VAGRANCY
# -----------------------------------------------------------------------------
echo "Stopping vagrancy..."
docker stop vagrancy_test
sudo rm -rf ${VAGRANCY_DATA_DIR}
echo "Vagrancy stopped."


exit $RETVAL


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
