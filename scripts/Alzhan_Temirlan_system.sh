#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
INFO_FILE="$PROJECT_DIR/Alzhan_Temirlan_info.txt"

printf '==============================\n'
printf 'Student Information\n'
printf '==============================\n'
printf 'Name: Temirlan\n'
printf 'Surname: Alzhan\n'
printf 'Group: IT2-2307\n'
printf 'Student ID: 38372\n'

printf '\n==============================\n'
printf 'System Information\n'
printf '==============================\n'

printf 'Username: '; whoami
printf 'Hostname: '; hostname
printf 'Current Date: '; date --iso-8601=seconds
printf 'Operating System: '; uname -a
printf '\nDisk Usage:\n'
df -h /
printf '\nMemory Usage:\n'
free -h

if [[ -f "$INFO_FILE" ]]; then
    echo 'Student information file exists.'
else
    echo 'Student information file does not exist.'
fi
