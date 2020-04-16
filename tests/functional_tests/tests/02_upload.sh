#!/bin/bash -e
# ----------------------------------------------------------------------------
# Check the upload function.
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
echo "1.2.3" > $BOXFILE
capture_output_success upload_first_version upload $BOXFILE base/test virtualbox 1.2.3
cmp $BOXFILE ${VAGRANCY_DATA_DIR}/base/test/1.2.3/virtualbox/box

capture_output_success upload_first_version_2 upload $BOXFILE base/test libvirt 1.2.3
cmp $BOXFILE ${VAGRANCY_DATA_DIR}/base/test/1.2.3/libvirt/box

# Upload the next version
echo "1.2.4" > $BOXFILE
capture_output_success upload_next_version  upload $BOXFILE base/test virtualbox
cmp $BOXFILE ${VAGRANCY_DATA_DIR}/base/test/1.2.4/virtualbox/box

# Upload the next version and delete all previous ones
capture_output_success upload_with_delete  upload --delete-other-versions $BOXFILE base/test libvirt
cmp $BOXFILE ${VAGRANCY_DATA_DIR}/base/test/1.2.4/libvirt/box
if [ -e ${VAGRANCY_DATA_DIR}/base/test/1.2.3/libvirt/box ]; then
    echo "ERROR: Previous box not deleted!"
    rm -f $BOXFILE
    exit 1
fi

# Upload with provider pattern (not allowed)
capture_output_failure upload_provider_pattern upload $BOXFILE base/test v*box

# Upload with multiple matching box names
echo "1.2.3" > $BOXFILE
capture_output_success upload_alternative upload $BOXFILE base/alternative virtualbox
capture_output_failure upload_multi_boxes upload $BOXFILE base/* virtualbox

# Upload with non-semantic versions fails
echo "1.2.3-alpha" > $BOXFILE
capture_output_success upload_non_semantic upload $BOXFILE base/non-semantic virtualbox 1.2.3-alpha
capture_output_failure upload_non_semantic_increment upload $BOXFILE base/non-semantic virtualbox

# Upload same version twice
echo "1.2.3" > $BOXFILE
capture_output_success upload_same_first  upload $BOXFILE base/same virtualbox 1.2.3
capture_output_success upload_same_second upload --delete-other-versions $BOXFILE base/same virtualbox 1.2.3
cmp $BOXFILE ${VAGRANCY_DATA_DIR}/base/same/1.2.3/virtualbox/box

rm -f $BOXFILE


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
