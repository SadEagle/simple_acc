#!/bin/sh

set -ex

ty check
ruff check
ruff format --check
