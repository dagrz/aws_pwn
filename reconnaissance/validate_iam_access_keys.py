#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import argparse

# BROKEN - NEEDS FIXING
def main(args):
    output = []
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
                output.append( validate_key(access_key_id, secret_access_key, session_token) )

    print(json.dumps(output, indent=2)) 


def validate_key(access_key_id, secret_access_key, session_token=None):
    client = boto3.client(
        'sts',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
    )
    
    output = {
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
        output['result'] = 'success' 
        output['accountId'] = response['Account']  
        output['userId'] = response['UserId']  
        output['arn'] = response['Arn']     
    except ClientError as e:
        output['error'] = e.response['Error']['Message']
    
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Validate AWS access keys and secrets.")
    parser.add_argument('-i',
                        '--input-file',
                        type=argparse.FileType('r'),
                        required=True)
    parser.add_argument('-o',
                    '--output-file',
                    type=argparse.FileType('w'))
    args = parser.parse_args()
    main(args)