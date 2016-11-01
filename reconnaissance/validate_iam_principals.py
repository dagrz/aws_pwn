#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import argparse
import uuid
from datetime import datetime


def main(args):
    all_results = []
    for line in args.input_file.readlines():
        line = line.strip()
        if(line and not line.startswith('#')):
            result = validate_principal('trust_policy', line)
            all_results.append(result)
            if result['exists']:
                print(json.dumps(result, indent=2))
    args.input_file.close()

    if(args.output_file is not None):
        args.output_file.write(json.dumps(all_results, indent=2))
        args.output_file.close()
            

def validate_principal(validation_type, principal_name):
    validation_functions = {
        'trust_policy': validate_principal_trust_policy
    }
    if validation_functions[validation_type]:
        return validation_functions[validation_type](principal_name)


def validate_principal_trust_policy(principal_name):
    # This test requires authentication
    # It also requires iam:createRole and iam:deleteRole permissions
    # Warning: Check credentials before use
    result = {
        'principalName': principal_name,
        'accountId': args.account_id,
        'arn': 'arn:aws:iam::' + args.account_id + ':' + principal_name,
        'exists': False,
        'error': None
    }

    client = boto3.client('iam')
    template_policy = """{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "",
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::ACCOUNT_ID:PRINCIPAL"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }"""
    
    try:
        test_role_name = 'test_role_{}'.format(uuid.uuid4())
        test_role_policy = template_policy.replace('ACCOUNT_ID', args.account_id).replace('PRINCIPAL', principal_name)
        response = client.create_role(
            RoleName=test_role_name,
            AssumeRolePolicyDocument=test_role_policy
        )
        result['exists'] = True
        try:
            client.delete_role(RoleName=test_role_name)
        except:
            pass
    except ClientError as e:
        result['error'] = e.response['Error']['Message']
    
    return result
    

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Validate existence of IAM principals (users, roles etc.) in a file.")
    parser.add_argument('-i',
                        '--input-file',
                        type=argparse.FileType('r'),
                        required=True)
    parser.add_argument('-o',
                        '--output-file',
                        type=argparse.FileType('w'))
    parser.add_argument('-a',
                        '--account-id',
                        required=True)
    args = parser.parse_args()
    main(args)