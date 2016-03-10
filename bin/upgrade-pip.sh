#!/bin/bash

PIP_MAJOR_VERSION=$(pip --version | cut -d ' ' -f 2 | cut -d '.' -f 1)

if [[ "$PIP_MAJOR_VERSION" != "8" ]]; then
  echo "Upgrading pip to version 8"
  bin/pipstrap.py
else
  echo "No need to upgrade pip"
fi
