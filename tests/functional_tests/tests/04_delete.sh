#!/bin/bash -e
# ----------------------------------------------------------------------------
# Check the delete function.
#
# Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
# All rights reserved.
# This file is part of vagrancyCtrl (https://github.com/seeraven/vagrancyCtrl)
# and is released under the "BSD 3-Clause License". Please see the LICENSE file
# that is included as part of this package.
# ----------------------------------------------------------------------------


EXPECTED_OUTPUT_PREFIX=$(basename $0 .sh)
source $TEST_BASE_DIR/helpers/output_helpers.sh


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------
BOXFILE=$(tempfile)

# Upload the initial box
echo "2.0.0" > $BOXFILE
capture_output_success upload_first_box     upload $BOXFILE base/dtest  virtualbox 2.0.0
capture_output_success upload_first_box_2   upload $BOXFILE base/dtest2 virtualbox 2.0.0

# Upload the next version
echo "2.0.1" > $BOXFILE
capture_output_success upload_next_box      upload $BOXFILE base/dtest virtualbox

# Delete info (no patterns)
capture_output_success delete_info_fix      delete -p virtualbox base/dtest 2.0.1
capture_output_success delete_info_old      delete -p virtualbox base/dtest -- -1
capture_output_success delete_info_vpattern delete -p virtualbox base/dtest 2.?.1
capture_output_success delete_info_ppattern delete -p v*box      base/dtest 2.0.1
capture_output_success delete_info_bpattern delete -p virtualbox base/dt??t 2.0.1

# Delete action
capture_output_success delete_old           delete -f -p virtualbox base/dtest -- -1
if [ -e ${VAGRANCY_DATA_DIR}/base/dtest/2.0.0/virtualbox ]; then
    echo "ERROR: Old version not deleted!"
    rm -f $BOXFILE
    exit 1
fi
capture_output_success delete_latest        delete -f -p virtualbox base/dtest -- +1
if [ -e ${VAGRANCY_DATA_DIR}/base/dtest/2.0.1/virtualbox ]; then
    echo "ERROR: Latest version not deleted!"
    rm -f $BOXFILE
    exit 1
fi

# No boxes found
capture_output_failure delete_nonexist      delete -f -p virtualbox base/dtest -- -1

rm -f $BOXFILE


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
