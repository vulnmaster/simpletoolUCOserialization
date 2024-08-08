#!/usr/bin/make -f

# Portions of this file contributed by NIST are governed by the
# following statement:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to Title 17 Section 105 of the
# United States Code, this software is not subject to copyright
# protection within the United States. NIST assumes no responsibility
# whatsoever for its use by other parties, and makes no guarantees,
# expressed or implied, about its quality, reliability, or any other
# characteristic.
#
# We would appreciate acknowledgement if the software is used.

SHELL := /bin/bash

top_srcdir := ..

all: \
  shared_hashes_framed.jsonld.case_validate.done.log \
  selfie_framed.jsonld.case_validate.done.log

%.jsonld.case_validate.done.log: \
  %.jsonld \
  $(top_srcdir)/.venv.done.log
	source $(top_srcdir)/venv/bin/activate \
	  && case_validate \
	    --allow-infos \
	    $<
	touch $@

.mypy.done.log: \
  $(top_srcdir)/.venv.done.log \
  frame.py
	source $(top_srcdir)/venv/bin/activate \
	  && mypy --strict frame.py
	touch $@

check: \
  all

clean:
	@rm -f \
	  *.case_validate.done.log \
	  *_framed.jsonld

selfie_framed.jsonld: \
  .mypy.done.log \
  case_file_frame.jsonld \
  selfie_flattened.jsonld.case_validate.done.log
	source $(top_srcdir)/venv/bin/activate \
	  && python3 frame.py \
	    __$@ \
	    case_file_frame.jsonld \
	    selfie_flattened.jsonld
	python3 -m json.tool __$@ _$@
	rm __$@
	mv _$@ $@

shared_hashes_framed.jsonld: \
  .mypy.done.log \
  case_file_frame.jsonld \
  shared_hashes_flattened.jsonld.case_validate.done.log
	source $(top_srcdir)/venv/bin/activate \
	  && python3 frame.py \
	    __$@ \
	    case_file_frame.jsonld \
	    shared_hashes_flattened.jsonld
	python3 -m json.tool __$@ _$@
	rm __$@
	mv _$@ $@
