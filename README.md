# AWS pwn

## Summary

This is a collection of horribly written scripts for performing various tasks related to penetration testing AWS. Please don't be sad if it doesn't work for you. It might be that AWS has changed since a given tool was written or it might be that the code sux. Either way, please feel free to contribute.

Most of this junk was written by Daniel Grzelak but there's been plenty of contributions, most notably Mike Fuller.

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
./validate_accounts.py -i /tmp/acounts.txt -o /tmp/out.json
```

## Exploitation

Things that will help you gain a foothold in an account.

## Stealth

Things that might help you stay hidden after compromising an account.

## Exploration

Things to help you understand what you've pwned.

## Elevation

Things to help you move around an account and gather different levels of access.

* dump_instance_attributes.py - Goes through every EC2 instance in the account and retrieves the specified instance attributes. Most commonly used to retrieve userData.
```
./dump_instance_attributes.py -u -o /tmp/
```
* assume_roles.py - Attempts to assume all roles (ARNs) in a file or provided by the list-roles API.
```
./assume_roles.py -o /tmp/out.json
```

## Persistence

Things to help maintain your access to an acccount.

* rabbit_lambda - An example Lambda function that responds to user delete events by creating more copies of the deleted user.

## Exfiltration

Things to help you extract and move data around in AWSy ways.

## Miscellanea

Other things that I was either to stupid or too lazy to classify.

* reserved_words.txt - A list of words/tokens that have some special meaning in AWS or are likely to soon have some special meaning.
* endpoints.txt - A somewhat up to date list of API endpoints exposed by AWS.
* integrations.txt - A TSV of services that integrate with AWS via roles or access keys and their account ids, default usernames etc.
* download_docs.sh - The command line to wget all the AWS docs because I'm stupid and waste time redoing it every time.

