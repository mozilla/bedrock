# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Makefile for MkDocs documentation

BUILDDIR      = site

.PHONY: help clean preflight serve build

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean      to remove all output files"
	@echo "  serve      to run MkDocs locally, live-rebuilding content as it changes"
	@echo "  preflight 	to install Python dependencies for documentation building"

clean:
	rm -rf $(BUILDDIR)/*

preflight:
	cd .. && uv sync --locked --active --python 3.13 --inexact --only-group docs

serve:
	mkdocs serve --open

build:
	mkdocs build
