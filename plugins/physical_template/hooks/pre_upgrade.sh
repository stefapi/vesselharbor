#!/bin/bash
#
# Copyright (c) 2025.  VesselHarbor
#
# ____   ____                          .__    ___ ___             ___.
# \   \ /   /____   ______ ______ ____ |  |  /   |   \_____ ______\_ |__   ___________
#  \   Y   // __ \ /  ___//  ___// __ \|  | /    ~    \__  \\_  __ \ __ \ /  _ \_  __ \
#   \     /\  ___/ \___ \ \___ \\  ___/|  |_\    Y    // __ \|  | \/ \_\ (  <_> )  | \/
#    \___/  \___  >____  >____  >\___  >____/\___|_  /(____  /__|  |___  /\____/|__|
#               \/     \/     \/     \/            \/      \/          \/
#
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#

# Pre-upgrade script for physical host or VM installation
# This script runs on the host machine before an upgrade

# Validate that required tools are available
command -v ssh >/dev/null 2>&1 || { echo "SSH client is required but not installed. Aborting."; exit 1; }
command -v scp >/dev/null 2>&1 || { echo "SCP is required but not installed. Aborting."; exit 1; }

# Get configuration from environment variables
HOST="${HOST:-localhost}"
PORT="${PORT:-22}"
USER="${USER:-root}"
APP_NAME="${APP_NAME:-app}"
INSTALL_DIR="${INSTALL_DIR:-/opt/app}"

# Check if we can connect to the host
echo "Checking connection to $HOST..."
ssh -p $PORT $USER@$HOST "echo 'Connection successful'" || { echo "Failed to connect to $HOST. Please check your connection settings."; exit 1; }

# Backup the current application
echo "Backing up the current application..."
BACKUP_DIR="/tmp/$APP_NAME-backup-$(date +%Y%m%d%H%M%S)"
ssh -p $PORT $USER@$HOST "mkdir -p $BACKUP_DIR && cp -r $INSTALL_DIR/* $BACKUP_DIR/ && echo 'Backup created at $BACKUP_DIR'"

echo "Pre-upgrade checks completed successfully."
