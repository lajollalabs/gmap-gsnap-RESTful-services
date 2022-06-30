#!/usr/bin/env python
import os
import sys



sys.path.append("/gmap/gmap-gsnap-RESTful-services/gscript/gmapr/gsnap_exec.py")
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djp.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
