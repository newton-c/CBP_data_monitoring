#!/usr/bin/python3

import logging
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
import os

s3 = boto3.client('s3')

# upload methampetamines plot
s3.upload_file('figs/meth.html', 'public-ic-resources', 'cbp_meth.html', ExtraArgs={'ContentType': 'text/html'})

#'ACL': 'public-read'

# upload fentanyl plot
s3.upload_file('figs/fentanyl.html', 'public-ic-resources', 'cbp_fentanyl.html', ExtraArgs={'ContentType': 'text/html'})
