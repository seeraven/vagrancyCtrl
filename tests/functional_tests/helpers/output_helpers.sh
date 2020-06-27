# ----------------------------------------------------------------------------
# Helper functions for the functional tests.
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
# ----------------------------------------------------------------------------

# Usage: capture_output <expected retval> <name> <args>
function capture_output()
{
    STDOUT_FILE=$(tempfile)
    STDERR_FILE=$(tempfile)

    EXPECTED_RETVAL=$1
    shift

    EXPECTED_STDOUT_FILE=${EXPECTED_OUTPUT_DIR}/${EXPECTED_OUTPUT_PREFIX}_$1_stdout.txt
    EXPECTED_STDERR_FILE=${EXPECTED_OUTPUT_DIR}/${EXPECTED_OUTPUT_PREFIX}_$1_stderr.txt
    shift

    set +e
    $VAGRANCYCTRL_BIN $@ > $STDOUT_FILE 2> $STDERR_FILE
    RETVAL=$?
    set -e

    if [ $RETVAL != $EXPECTED_RETVAL ]; then
	echo "ERROR: Command vagrancyCtrl $@ gave unexpected return value $RETVAL (expected ${EXPECTED_RETVAL})"
	RETVAL=10
    else
	RETVAL=0
    fi

    if [ "$SAVE_REFERENCE" == "1" ]; then
	cp $STDOUT_FILE $EXPECTED_STDOUT_FILE
	cp $STDERR_FILE $EXPECTED_STDERR_FILE
    else
	if ! cmp -s $STDOUT_FILE $EXPECTED_STDOUT_FILE; then
	    echo "ERROR: Command vagrancyCtrl $@ gave unexpected stdout output:"
	    cat $STDOUT_FILE
	    echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	    echo "Diff:"
	    diff $STDOUT_FILE $EXPECTED_STDOUT_FILE
	    echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	    RETVAL=10
	fi
	if ! cmp -s $STDERR_FILE $EXPECTED_STDERR_FILE; then
	    echo "ERROR: Command vagrancyCtrl $@ gave unexpected sterr output:"
	    cat $STDERR_FILE
	    echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	    echo "Diff:"
	    diff $STDERR_FILE $EXPECTED_STDERR_FILE
	    echo "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	    RETVAL=10
	fi
    fi

    rm -f $STDOUT_FILE $STDERR_FILE

    return $RETVAL
}

# Usage: capture_output_success <name> <args>
function capture_output_success()
{
    capture_output 0 $@
}

# Usage: capture_output_failure <name> <args>
function capture_output_failure()
{
    capture_output 1 $@
}

# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
