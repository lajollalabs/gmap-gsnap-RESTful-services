#!/bin/bash
export PYTHONPATH=/gmap/gmap-gsnap-RESTful-services:/gmap/gmap-gsnap-RESTful-services/gscript/gmapr:/gmap/gmap-gsnap-RESTful-services/gscript/bedtools
export PATH=$PATH:/gmap/gmap-gsnap-RESTful-services/gscript
python3 manage.py runserver 0.0.0.0:8000
