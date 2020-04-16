#!/bin/bash -e
# ----------------------------------------------------------------------------
# Check the usage output.
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
capture_output_failure noarg
capture_output_success main -h
capture_output_success delete delete -h
capture_output_success download download -h
capture_output_success print print -h
capture_output_success upload upload -h


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
