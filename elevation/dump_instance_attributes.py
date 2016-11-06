#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import base64
import argparse
import os
from datetime import datetime


REGIONS = [
    'ap-northeast-2',
    'ap-northeast-1',
    'ap-south-1',
    'ap-southeast-1',
    'ap-southeast-2',
    'cn-north-1',
    'eu-central-1',
    'eu-west-1',
    'sa-east-1',
    'us-east-1',
    'us-east-2',
    'us-west-1',
    'us-west-2',
    'us-gov-west-1'
]


def main(args):
    if args.attributes:
        for region in REGIONS:
            process_region(region)


def process_region(region_name):
    region_path = os.path.join(args.output_path, region_name)
    if not os.path.exists(region_path):
        os.makedirs(region_path)

    ec2 = boto3.resource(service_name='ec2', region_name=region_name)
    for instance in ec2.instances.all():
        process_instance(instance, region_path)


def process_instance(instance, region_path):
    for attribute in args.attributes:
        response = None
        try:
            response = instance.describe_attribute(Attribute=attribute)
        except ClientError as e:
            print(e.response['Error']['Message'])
            with open(os.path.join(region_path, instance.instance_id + '_' + attribute + '.error'), 'w') as attribute_error_file:
                 attribute_error_file.write(e.response['Error']['Message']) 
        
        if response:
            # Decode userData because it's base64 encoded
            if attribute == 'userData' and 'UserData' in response and 'Value' in response['UserData']:
                response['UserData']['Value'] = base64.b64decode(response['UserData']['Value'])
            if 'ResponseMetadata' in response:
                del response['ResponseMetadata']
            attribute_data = json.dumps(response, indent=2, default=json_serial)
            print(attribute_data)
            with open(os.path.join(region_path, instance.instance_id + '_' + attribute + '.json'), 'w') as attribute_data_file:
                 attribute_data_file.write(attribute_data)  


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
    parser.add_argument('-b',
                    '--block-device-mapping',
                    dest='attributes', 
                    action='append_const', 
                    const='blockDeviceMapping')
    parser.add_argument('-d',
                    '--disable-api-termination',
                    dest='attributes', 
                    action='append_const', 
                    const='disableApiTermination')
    parser.add_argument('-e',
                    '--ebs-optimized',
                    dest='attributes', 
                    action='append_const', 
                    const='ebsOptimized')
    parser.add_argument('-f',
                    '--ena-support',
                    dest='attributes', 
                    action='append_const', 
                    const='enaSupport')
    parser.add_argument('-g',
                    '--group-set',
                    dest='attributes', 
                    action='append_const', 
                    const='groupSet')
    parser.add_argument('-i',
                    '--instance-initiated-shutdown-behavior',
                    dest='attributes', 
                    action='append_const', 
                    const='instanceInitiatedShutdownBehavior')
    parser.add_argument('-j',
                    '--instance-type',
                    dest='attributes', 
                    action='append_const', 
                    const='instanceType')
    parser.add_argument('-k',
                    '--kernel',
                    dest='attributes', 
                    action='append_const', 
                    const='kernel')
    parser.add_argument('-p',
                    '--product-codes',
                    dest='attributes', 
                    action='append_const', 
                    const='productCodes')
    parser.add_argument('-r',
                    '--ramdisk',
                    dest='attributes', 
                    action='append_const', 
                    const='ramdisk')
    parser.add_argument('-s',
                    '--root-device-name',
                    dest='attributes', 
                    action='append_const', 
                    const='rootDeviceName')
    parser.add_argument('-t',
                    '--source-dest-check',
                    dest='attributes', 
                    action='append_const', 
                    const='sourceDestCheck')
    parser.add_argument('-v',
                    '--sriov-net-support',
                    dest='attributes', 
                    action='append_const', 
                    const='sriovNetSupport')
    parser.add_argument('-u',
                    '--user-data',
                    dest='attributes', 
                    action='append_const', 
                    const='userData')
    args = parser.parse_args()
    main(args)
