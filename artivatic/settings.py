try:
   from local_settings import *
except ImportError:
    raise Exception("A local_settings.py file is required to run this project")