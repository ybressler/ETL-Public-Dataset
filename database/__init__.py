from .connect import ConnectDb
from .metadata import metadata

# Create your database connection here
session = ConnectDb().session

from . import models
