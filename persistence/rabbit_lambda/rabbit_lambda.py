#!/usr/bin/env python
from __future__ import print_function
import json
import boto3
import random
import re
import string

USER_FORMAT_RE = r'^rabbit-\d{10}$'
USER_FORMAT_PREFIX = 'rabbit-'


def lambda_handler(event, context):
    if event['detail']['eventName'] == 'DeleteUser':
        deletedUser = event['detail']['requestParameters']['userName']
        if re.match(USER_FORMAT_RE, deletedUser, re.M|re.I):
            client = boto3.client('iam')
            newUser = USER_FORMAT_PREFIX + ''.join(random.choice(string.digits) for _ in range(10))
            client.create_user(UserName = newUser)
            newUser = USER_FORMAT_PREFIX + ''.join(random.choice(string.digits) for _ in range(10))
            client.create_user(UserName = newUser)
    return None
    
    
if __name__ == '__main__':
    event = {
        "account":"123456789012",
        "region":"us-east-1",
        "detail":{
            "eventVersion":"1.02",
            "eventID":"fb2a5c74-1234-1234-1234-1234560ddaf2",
            "eventTime":"2016-06-26T02:06:50Z",
            "requestParameters":{
                "userName":USER_FORMAT_PREFIX + "1234567890"
            },
            "eventType":"AwsApiCall",
            "responseElements": None,
            "awsRegion":"us-east-1",
            "eventName":"DeleteUser",
            "userIdentity":{
                "principalId":"123456789012",
                "accessKeyId":"ABCDEFGHIJKLMNOPQRST",
                "sessionContext":{
                    "attributes":{
                        "creationDate":"2016-06-26T00:57:02Z",
                        "mfaAuthenticated":"true"
                    }
                },
                "type":"Root",
                "arn":"arn:aws:iam::123456789012:root",
                "accountId":"123456789012"
            },
            "eventSource":"iam.amazonaws.com",
            "requestID":"a53939f5-1234-1234-1234-35e68685372d",
            "userAgent":"console.amazonaws.com",
            "sourceIPAddress":"1.2.3.4"
        },
        "detail-type":"AWS API Call via CloudTrail",
        "source":"aws.iam",
        "version":"0",
        "time":"2016-06-26T02:06:50Z",
        "id":"e6209d69-1234-1234-1234-a347e6ad8dd4",
        "resources":[

        ]
    }
    print(lambda_handler(event, None))