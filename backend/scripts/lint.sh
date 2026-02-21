#!/usr/bin/env bash

set -e
set -x

basedpyright app
ruff check app
ruff format app --check
