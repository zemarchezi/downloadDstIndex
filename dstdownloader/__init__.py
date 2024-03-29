import os

try:
  VERSION_PATH = os.path.join(os.path.dirname(__file__), "VERSION.txt")

  with open(VERSION_PATH, "r") as version_file:
    VERSION = version_file.read().strip()
except:
  import importlib.metadata
  VERSION = importlib.metadata.version('dstdownloader')


__version__ = VERSION
__license__ = "GPL-3.0 license"
__author__ = "José Paulo Marchezi"
__status__ = "Development"
# %%
