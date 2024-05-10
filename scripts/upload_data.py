#!/usr/bin/python3

import logging
import boto3
from botocore.exceptions import ClientError
import os

s3 = boto3.client('s3')

"""
The following commands need a few more elements before they'll
run. The need the 'BUCKET_NAME' AND 'OBJECT_NAME', and then I
think they'll need credentials, such as

ExtraArgs={
        'GrantRead': 'uri="http://acs.amazonaws.com/groups/global/AllUsers"',
        'GrantFullControl': 'id="01234567890abcdefg"',
    }
    
"""

# upload methampetamines plot
s3.upload_file('figs/meth.html')

# upload fentanyl plot
s3.upload_file('figs/fentanyl.html')
