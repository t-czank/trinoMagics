import re

import trino
from trino.auth import BasicAuthentication
from trino.dbapi import connect

# Create Trino connection function
def get_trino_connection():
    return trino.dbapi.connect(
    host='lakehouse.unext.dev',
    port=443,
    catalog='lakehouse',
    schema='unext_log',
    user='readonly',
    auth=BasicAuthentication("readonly", TRINO_READONLY_PASSWORD),
    http_scheme="https"
    )
