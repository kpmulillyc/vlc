#!/var/pythonapps/py3/bin/python3
import os, sys 

PROJECT_DIR = '/var/pythonapps/vlc'
sys.path.insert(0, PROJECT_DIR)


def execfile(filename):
    globals = dict( __file__ = filename )
    exec( open(filename).read(), globals )

activate_this = '/var/pythonapps/py3/bin/activate_this.py'
execfile( activate_this )



from test import app as application
application.debug = True
