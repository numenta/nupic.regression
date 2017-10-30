#!/bin/bash
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2016, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# -----------------------------------------------------------------------------

# Install what's necessary on top of raw Ubuntu for testing a NuPIC wheel.
#
# NOTE much of this will eventually go into a docker image

set -o errexit
set -o xtrace

# Install git, which may be necessary
apt-get install -y git-core

echo "Clone nupic..."
if [ ! -d "nupic" ]; then
    git clone https://github.com/numenta/nupic.git --depth 50
fi

echo "Installing NuPIC..."
pip install nupic-*.whl

echo "Clone NAB..."
if [ ! -d "NAB" ]; then
    git clone https://github.com/numenta/NAB.git --depth 50
fi

echo "Installing NAB..."
(cd NAB && python setup.py install)