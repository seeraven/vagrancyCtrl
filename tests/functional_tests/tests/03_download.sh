#!/bin/bash -e
# ----------------------------------------------------------------------------
# Check the download function.
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
capture_output_success upload_first_box     upload $BOXFILE base/test  virtualbox 2.0.0
capture_output_success upload_first_box_2   upload $BOXFILE base/test2 virtualbox 2.0.0

# Upload the next version
echo "2.0.1" > $BOXFILE
capture_output_success upload_next_box    upload $BOXFILE base/test virtualbox

# Download the oldest one
capture_output_success download_first_box download $BOXFILE base/test virtualbox 2.0.0
cmp $BOXFILE ${VAGRANCY_DATA_DIR}/base/test/2.0.0/virtualbox/box

# Download the latest one
capture_output_success download_next_box  download $BOXFILE base/test virtualbox
cmp $BOXFILE ${VAGRANCY_DATA_DIR}/base/test/2.0.1/virtualbox/box

# Download the latest one to stdout
capture_output_success download_next_box_stdout download - base/test virtualbox

# Download using patterns
capture_output_success download_patterns  download $BOXFILE base/test v*box 2.*0
cmp $BOXFILE ${VAGRANCY_DATA_DIR}/base/test/2.0.0/virtualbox/box

# Download a non-existant box
capture_output_failure download_non_exist download $BOXFILE base/nonexistant virtualbox

# Download multiple matching boxes
capture_output_failure download_multiboxes download $BOXFILE base/test* virtualbox

# Download no matching version
capture_output_failure download_no_version download $BOXFILE base/test v*box 3.*

# Download multiple matching versions
capture_output_failure download_multiversions download $BOXFILE base/test v*box 2.*

rm -f $BOXFILE


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
