import decimal
import logging
logging.basicConfig()
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import boto3
import time
from datetime import date

class DBRef:
    def __init__(self):
        self.logger = logging.getLogger('LIONDB')
        self.logger.info(' Loading %s\n'%(LIONDB_RESOURCE))

