#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import argparse
import time
import random
import uuid


ALL_POLICY = '''{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt''' + str(random.randint(100000, 999999)) +'''",
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
'''


def main(args):
    if args.user_name:
        attach_policy(args.user_name, 'UserName')
        put_policy(args.user_name, 'UserName')
    elif args.role_name:
        attach_policy(args.role_name, 'RoleName')
        put_policy(args.role_name, 'RoleName')
    elif args.group_name:
        attach_policy(args.group_name, 'GroupName')
        put_policy(args.group_name, 'GroupName')
    else:
        print('No user, role, or group specified. Quitting.')


def attach_policy(principal, principal_name):
    result = False
    client = boto3.client('iam')
    attach_policy_funcs = {
        'UserName': client.attach_user_policy,
        'RoleName': client.attach_role_policy,
        'GroupName': client.attach_group_policy
    }
    attach_policy_func = attach_policy_funcs[principal_name]
    try:
        response = attach_policy_func(**{
                principal_name: principal,
                'PolicyArn': 'arn:aws:iam::aws:policy/AdministratorAccess'
            }
        )
        result = True
        print('AdministratorAccess policy attached successfully to ' + principal)
    except ClientError as e:
        print(e.response['Error']['Message'])
    return result 


def put_policy(principal, principal_name):
    result = False
    client = boto3.client('iam')
    put_policy_funcs = {
        'UserName': client.put_user_policy,
        'RoleName': client.put_role_policy,
        'GroupName': client.put_group_policy
    }
    put_policy_func = put_policy_funcs[principal_name]
    try:
        response = put_policy_func(**{
                principal_name: principal,
                'PolicyName': str(uuid.uuid4()),
                'PolicyDocument': ALL_POLICY
            }
        )
        result = True
        print('All action policy attached successfully to ' + principal)
    except ClientError as e:
        print(e.response['Error']['Message'])
    return result   


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Attempts to add an admin and all actions policy to the given role, user, or group.")
    parser.add_argument('-u',
                        '--user-name')
    parser.add_argument('-r',
                        '--role-name')
    parser.add_argument('-g',
                        '--group-name')
    args = parser.parse_args()
    main(args)