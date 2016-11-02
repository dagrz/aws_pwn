#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import base64
import argparse
import os
from datetime import datetime


def main(args):
    client = boto3.client('cloudformation')
    response = None
    next_token = None
    stacks = []
    
    try:
        while (response is None or 'NextToken' in response):
            if next_token is None:
                response = client.list_stacks()
            else:
                response = client.list_stacks(NextToken=next_token)        
            stacks += response['StackSummaries']
            if 'NextToken' in response:
                next_token = response['NextToken']
    except ClientError as e:
        print(e.response['Error']['Message']) 

    for stack in stacks:
        process_stack(stack['StackName'], stack['StackId'])
    
    
def process_stack(stack_name, stack_id):
    client = boto3.client('cloudformation')
    response = None
    try:
        response = client.describe_stacks(StackName=stack_id)
    except ClientError as e:
        print(e.response['Error']['Message']) 

    if response:
        if 'ResponseMetadata' in response:
            del response['ResponseMetadata']
        stack_description = json.dumps(response, indent=2, default=json_serial)
        print(stack_description)
        with open(os.path.join(args.output_path, stack_name + '-' + stack_id.split('/')[-1] + '.json'), 'w') as stack_description_data_file:
             stack_description_data_file.write(stack_description)  


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dumps userData for all EC2 instances.")
    parser.add_argument('-o',
                    '--output-path',
                    default=os.path.curdir)

    args = parser.parse_args()
    main(args)
