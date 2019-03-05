#!/usr/bin/env bash

set -euxo pipefail

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

sudo apt install python3 python3-venv

python3 -m venv "$DIR/venv"
source ./venv/bin/activate

pip3 install -r requirements.txt
