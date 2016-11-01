#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import argparse


def main(args):
    all_results = []
    for line in args.input_file.readlines():
        line = line.strip()
        if(line and not line.startswith('#')):
            parts = line.split()
            access_key_id = secret_access_key = session_token = None
            if (len(parts) >= 2):
                access_key_id = parts[0]
                secret_access_key = parts[1]
                if (len(parts) >= 3):
                    session_token = parts[2]
                result = validate_key('caller_identity', access_key_id, secret_access_key, session_token)
                all_results.append(result)
                if result['result'] == 'success':
                    print(json.dumps(result, indent=2))
    args.input_file.close()

    if(args.output_file is not None):
        args.output_file.write(json.dumps(all_results, indent=2))
        args.output_file.close()


def validate_key(validation_type, access_key_id, secret_access_key, session_token=None):
    validation_functions = {
        'caller_identity': validate_key_caller_identity
    }
    if validation_functions[validation_type]:
        return validation_functions[validation_type](access_key_id, secret_access_key, session_token)    


def validate_key_caller_identity(access_key_id, secret_access_key, session_token=None):
    client = boto3.client(
        'sts',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
    )
    
    result = {
        'result': 'failure',
        'error': None,
        'accessKeyId': access_key_id,
        'secretAccessKey': secret_access_key,
        'sessionToken': session_token,
        'accountId': None,
        'userId': None,
        'arn': None     
    }

    try:
        response = client.get_caller_identity()
        result['result'] = 'success' 
        result['accountId'] = response['Account']  
        result['userId'] = response['UserId']  
        result['arn'] = response['Arn']     
    except ClientError as e:
        result['error'] = e.response['Error']['Message']
    
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Validate AWS access keys and secrets in a TSV.")
    parser.add_argument('-i',
                        '--input-file',
                        type=argparse.FileType('r'),
                        required=True)
    parser.add_argument('-o',
                        '--output-file',
                        type=argparse.FileType('w'))
    args = parser.parse_args()
    main(args)