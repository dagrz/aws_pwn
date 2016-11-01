#!/usr/bin/env python
from __future__ import print_function
import json
import argparse
import re
import requests
import validators


def main(args):
    all_results = []
    for line in args.input_file.readlines():
        line = line.strip()
        if(line and not line.startswith('#')):
            result = validate_account('signin', line)
            all_results.append(result)
            if result['exists']:
                print(json.dumps(result, indent=2))
    args.input_file.close()

    if(args.output_file is not None):
        args.output_file.write(json.dumps(all_results, indent=2))
        args.output_file.close()
            

def validate_account(validation_type, account):
    validation_functions = {
        'signin': validate_account_signin
    }
    if validation_functions[validation_type]:
        return validation_functions[validation_type](account)


def validate_account_signin(account):
    result = {
        'accountAlias': None,
        'accountId': None,
        'signinUri': 'https://' + account + '.signin.aws.amazon.com/',
        'exists': False,
        'error': None
    }

    if re.match(r'\d{12}', account):
        result['accountId'] = account
    else:
        result['accountAlias'] = account

    if not validators.url(result['signinUri']):
        result['error'] = 'Invalid URI'
        return result

    try:
        r = requests.get(result['signinUri'], allow_redirects=False)
        if r.status_code == 302:
            result['exists'] = True
    except requests.exceptions.RequestException as e:
        result['error'] = e

    return result
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Validate existence of an account ID or account alias.")
    parser.add_argument('-i',
                        '--input-file',
                        type=argparse.FileType('r'),
                        required=True)
    parser.add_argument('-o',
                        '--output-file',
                        type=argparse.FileType('w'))
    args = parser.parse_args()
    main(args)