#!/usr/bin/env python
from __future__ import print_function
import boto3
import base64
import argparse
import os


def main(args):
    client = boto3.client(service_name='ec2', region_name='us-east-1')
    for region in client.describe_regions()['Regions']:
        region_path = os.path.join(os.path.curdir, region['RegionName'])
        if not os.path.exists(region_path):
            os.makedirs(region_path)
        ec2 = boto3.resource(service_name='ec2', region_name=region['RegionName'])
        for instance in ec2.instances.all():
            response = instance.describe_attribute(Attribute='userData')
            if 'UserData' in response and response['UserData']:
                with open(os.path.join(region_path, instance.instance_id), 'w') as user_data_file:
                    user_data_file.write(base64.b64decode(response['UserData']['Value']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dumps userData for all EC2 instances")
    args = parser.parse_args()
    main(args)
