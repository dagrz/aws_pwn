#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json
import argparse


def main(args):



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Validates existence of s3 buckets and enumerates their permissions.")
    parser.add_argument('-f',
                        '--input-file',
                        type=argparse.FileType('r'),
                        default='buckets.txt')
    args = parser.parse_args()
    main(args)