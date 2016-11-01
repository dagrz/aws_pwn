#!/usr/bin/env python

from __future__ import print_function
import awscli
import awscli.clidriver
from cStringIO import StringIO
import sys
import json


def lambda_handler(event, context):
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    driver = awscli.clidriver.create_clidriver()
    driver.main(args=event["command"])

    sys.stdout = old_stdout

    return json.loads(mystdout.getvalue())
    
    
if __name__ == '__main__':
    event = {
        "command": [
            "sts",
            "get-caller-identity"
        ]
    }
    print(lambda_handler(event, None))