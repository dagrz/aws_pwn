# AWS pwn

## Summary

This is a collection of horribly written scripts for performing various tasks related to penetration testing AWS. Please don't be sad if it doesn't work for you. It might be that AWS has changed since a given tool was written or it might be that the code sux. Either way, please feel free to contribute.

Most of this junk was written by Daniel Grzelak but there's been plenty of contributions, most notably Mike Fuller.

## Reconnaissance

Things to do with pre-compromise information gathering.

* validate_iam_access_keys.py - Given a TSV file of access key + secret [+ session] combinations, checks access validity and returns identity information of the principal.
* validate_s3_buckets.py - Given a text file with one word per line, checks whether the buckets exist and returns basic identifying information.

## Exploitation

Things that will help you gain a foothold in an account.

## Stealth

Things that might help you stay hidden after compromising an account.

## Exploration

Things to help you understand what you've pwned.

## Elevation

Things to help you move around an account and gather different levels of access.

* dump_instance_attributes.py - Goes through every EC2 instance in the account and retrieves the specified instance attributes. Most commonly used to retrieve userData.

## Persistence

Things to help maintain your access to an acccount.

## Exfiltration

Things to help you extract and move data around in AWSy ways.

## Miscellanea

Other things that I was either to stupid or too lazy to classify.

* reserved_words.txt - A list of words/tokens that have some special meaning in AWS or are likely to soon have some special meaning.
* endpoints.txt - A somewhat up to date list of API endpoints exposed by AWS.

