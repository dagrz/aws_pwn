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
            result = validate_bucket('head', line)
            all_results.append(result)
            if result['exists']:
                print(json.dumps(result, indent=2))
    args.input_file.close()

    if(args.output_file is not None):
        args.output_file.write(json.dumps(all_results, indent=2))
        args.output_file.close()
            

def validate_bucket(validation_type, bucket_name):
    validation_functions = {
        'head': validate_bucket_head
    }
    if validation_functions[validation_type]:
        return validation_functions[validation_type](bucket_name)


def validate_bucket_head(bucket_name):
    # This test requires authentication
    # Warning: Check credentials before use
    error_values = {
        '400': True,
        '403': True,
        '404': False
    }
    result = {
        'bucketName': bucket_name,
        'bucketUri': 'http://' + bucket_name + '.s3.amazonaws.com',
        'arn': 'arn:aws:s3:::' + bucket_name,
        'exists': False
    }

    client = boto3.client('s3')
    try:
        client.head_bucket(Bucket=bucket_name)
        result['exists'] = True
    except ClientError as e:
        result['exists'] = error_values[e.response['Error']['Code']]
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Validate existence of s3 buckets in a file.")
    parser.add_argument('-i',
                        '--input-file',
                        type=argparse.FileType('r'),
                        required=True)
    parser.add_argument('-o',
                        '--output-file',
                        type=argparse.FileType('w'))
    args = parser.parse_args()
    main(args)