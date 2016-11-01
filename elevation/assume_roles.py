#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import argparse
import uuid


def main(args):
    all_results = []
    
    if(args.input_file is not None):
        for line in args.input_file.readlines():
            line = line.strip()
            if(line and not line.startswith('#')):
                result = attempt_assume_role(line)
                all_results.append(result)
                if result['result'] == 'success':
                    print(json.dumps(result, indent=2))
        args.input_file.close()
    else:
        role_arns = get_role_arns()
        for role_arn in role_arns:               
            result = attempt_assume_role(role_arn)
            all_results.append(result)
            if result['result'] == 'success':
                print(json.dumps(result, indent=2))


    if(args.output_file is not None):
        args.output_file.write(json.dumps(all_results, indent=2))
        args.output_file.close()


def get_role_arns():
    client = boto3.client('iam')
    response = None
    role_arns = []
    marker = None
    
    try:
        # By default, only 100 roles are returned at a time.
        # 'Marker' is used for pagination.
        while (response is None or response['IsTruncated']):
            # Marker is only accepted if result was truncated.
            if marker is None:
                response = client.list_roles()
            else:
                response = client.list_roles(Marker=marker)        

            roles = response['Roles']
            for role in roles:
                role_arns.append(role['Arn'])

            if response['IsTruncated']:
                marker = response['Marker']
    except ClientError as e:
        print(e.response['Error']['Message'])

    return role_arns


def get_inline_role_policies(role_name):
    client = boto3.client('iam')
    response = None
    role_policy_names = []
    marker = None
    
    try:
        # By default, only 100 roles are returned at a time.
        # 'Marker' is used for pagination.
        while (response is None or response['IsTruncated']):
            # Marker is only accepted if result was truncated.
            if marker is None:
                response = client.list_role_policies(RoleName=role_name)
            else:
                response = client.list_role_policies(RoleName=role_name, Marker=marker)        

            role_policies = response['PolicyNames']
            for role_policy in role_policies:
                role_policy_names.append(role_policy)

            if response['IsTruncated']:
                marker = response['Marker']
    except ClientError as e:
        pass

    return role_policy_names  


def get_managed_role_policies(role_name):
    client = boto3.client('iam')
    response = None
    role_policy_names = []
    marker = None
    
    try:
        # By default, only 100 roles are returned at a time.
        # 'Marker' is used for pagination.
        while (response is None or response['IsTruncated']):
            # Marker is only accepted if result was truncated.
            if marker is None:
                response = client.list_attached_role_policies(RoleName=role_name)
            else:
                response = client.list_attached_role_policies(RoleName=role_name, Marker=marker)        

            role_policies = response['AttachedPolicies']
            for role_policy in role_policies:
                role_policy_names.append(role_policy['PolicyName'])

            if response['IsTruncated']:
                marker = response['Marker']
    except ClientError as e:
        pass

    return role_policy_names   


def attempt_assume_role(role_arn):
    result = {
        "arn": role_arn,
        "roleName": role_arn.split(':')[-1].split('/')[-1],
        "result": 'failure',
        "roleId": None,
        "accessKeyId": None,
        "secretAccessKey": None,
        "sessionToken": None,
        "error": None,
        "rolePolicies": []
    }

    client = boto3.client('sts')

    try:
        response = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=str(uuid.uuid4())
        )
        result['result'] = 'success'
        result['roleId'] = response['AssumedRoleUser']['AssumedRoleId']
        result['accessKeyId'] = response['Credentials']['AccessKeyId']
        result['secretAccessKey'] = response['Credentials']['SecretAccessKey']
        result['sessionToken'] = response['Credentials']['SessionToken']
        inline_policies = get_inline_role_policies(result['roleName'])
        managed_policies = get_managed_role_policies(result['roleName'])
        result['rolePolicies'] = inline_policies + managed_policies
    except ClientError as e:
        result['error'] = e.response['Error']['Message'] 
    
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Attemps to assume all roles in a file or returned by list-roles API.")
    parser.add_argument('-i',
                        '--input-file',
                        type=argparse.FileType('r'))
    parser.add_argument('-o',
                        '--output-file',
                        type=argparse.FileType('w'))
    args = parser.parse_args()
    main(args)