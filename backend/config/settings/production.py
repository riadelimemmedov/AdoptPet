from decouple import config

from ..base import *

#!Debug
DEBUG = False


#!DATABASES
# ?Not Touch this line,because not configutation docker image,use only local
# DATABASES = {
#     "default": {
#       Using docker postgres image
#     }
# }


#!Installed Apps
INSTALLED_APPS += []


#!Middleware
MIDDLEWARE += []
