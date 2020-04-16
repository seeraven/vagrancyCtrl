#!/bin/bash -e
# ----------------------------------------------------------------------------
# Check the print function.
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
capture_output_success print_csv_all                  print --csv
capture_output_success print_csv_box_pattern          print --csv base/dtest*
capture_output_success print_csv_provider_pattern     print --csv --provider v*box

capture_output_success print_verbose_all              print --verbose
capture_output_success print_verbose_box_pattern      print --verbose base/dtest*
capture_output_success print_verbose_provider_pattern print --verbose --provider v*box

capture_output_success print_all                      print
capture_output_success print_box_pattern              print base/dtest*
capture_output_success print_provider_pattern         print --provider v*box


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
