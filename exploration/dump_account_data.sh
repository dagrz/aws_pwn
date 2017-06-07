#!/bin/sh
if [ $# -eq 0 ]
  then
    mkdir account-data
    cd account-data
else
  mkdir $1
  cd $1
fi

# https://docs.aws.amazon.com/cli/latest/reference/iam/index.html
###
# https://docs.aws.amazon.com/cli/latest/reference/iam/get-account-authorization-details.html
aws iam get-account-authorization-details > iam-get-account-authorization-details.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/get-account-password-policy.html
aws iam get-account-password-policy > iam-get-account-password-policy.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/get-account-summary.html
aws iam get-account-summary > iam-get-account-summary.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/list-account-aliases.html
aws iam list-account-aliases > iam-list-account-aliases.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/list-groups.html
aws iam list-groups > iam-list-groups.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/list-instance-profiles.html
aws iam list-instance-profiles > iam-list-instance-profiles.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/list-open-id-connect-providers.html
aws iam list-open-id-connect-providers > iam-list-open-id-connect-providers.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/list-policies.html
aws iam list-policies > iam-list-policies.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/list-roles.html
aws iam list-roles > iam-list-roles.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/list-saml-providers.html
aws iam list-saml-providers > iam-list-saml-providers.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/list-server-certificates.html
aws iam list-server-certificates > iam-list-server-certificates.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/list-users.html
aws iam list-users > iam-list-users.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/list-virtual-mfa-devices.html
aws iam list-virtual-mfa-devices > iam-list-virtual-mfa-devices.json
# https://docs.aws.amazon.com/cli/latest/reference/iam/get-credential-report.html
aws iam get-credential-report > iam-get-credential-report.json

# https://docs.aws.amazon.com/cli/latest/reference/ec2/index.html
###
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-account-attributes.html
aws ec2 describe-account-attributes > ec2-describe-account-attributes.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-addresses.html
aws ec2 describe-addresses > ec2-describe-addresses.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-bundle-tasks.html
aws ec2 describe-bundle-tasks > ec2-describe-bundle-tasks.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-classic-link-instances.html
aws ec2 describe-classic-link-instances > ec2-describe-classic-link-instances.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-conversion-tasks.html
aws ec2 describe-conversion-tasks > ec2-describe-conversion-tasks.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-customer-gateways.html
aws ec2 describe-customer-gateways > ec2-describe-customer-gateways.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-dhcp-options.html
aws ec2 describe-dhcp-options > ec2-describe-dhcp-options.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-export-tasks.html
aws ec2 describe-export-tasks > ec2-describe-export-tasks.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-flow-logs.html
aws ec2 describe-flow-logs > ec2-describe-flow-logs.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-host-reservations.html
aws ec2 describe-host-reservations > ec2-describe-host-reservations.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-hosts.html
aws ec2 describe-hosts > ec2-describe-hosts.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-images.html
aws ec2 describe-images > ec2-describe-images.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-import-image-tasks.html
aws ec2 describe-import-image-tasks > ec2-describe-import-image-tasks.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-import-snapshot-tasks.html
aws ec2 describe-import-snapshot-tasks > ec2-describe-import-snapshot-tasks.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instance-status.html
aws ec2 describe-instance-status > ec2-describe-instance-status.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html
aws ec2 describe-instances > ec2-describe-instances.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-internet-gateways.html
aws ec2 describe-internet-gateways > ec2-describe-internet-gateways.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-key-pairs.html
aws ec2 describe-key-pairs > ec2-describe-key-pairs.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-moving-addresses.html
aws ec2 describe-moving-addresses > ec2-describe-moving-addresses.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-nat-gateways.html
aws ec2 describe-nat-gateways > ec2-describe-nat-gateways.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-network-acls.html
aws ec2 describe-network-acls > ec2-describe-network-acls.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-network-interfaces.html
aws ec2 describe-network-interfaces > ec2-describe-network-interfaces.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-placement-groups.html
aws ec2 describe-placement-groups > ec2-describe-placement-groups.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-reserved-instances.html
aws ec2 describe-reserved-instances > ec2-describe-reserved-instances.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-reserved-instances-listings.html
aws ec2 describe-reserved-instances-listings > ec2-describe-reserved-instances-listings.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-reserved-instances-modifications.html
aws ec2 describe-reserved-instances-modifications > ec2-describe-reserved-instances-modifications.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-route-tables.html
aws ec2 describe-route-tables > ec2-describe-route-tables.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-scheduled-instances.html
aws ec2 describe-scheduled-instances > ec2-describe-scheduled-instances.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-security-groups.html
aws ec2 describe-security-groups > ec2-describe-security-groups.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-snapshots.html
aws ec2 describe-snapshots > ec2-describe-snapshots.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-spot-datafeed-subscription.html
aws ec2 describe-spot-datafeed-subscription > ec2-describe-spot-datafeed-subscription.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-spot-fleet-requests.html
aws ec2 describe-spot-fleet-requests > ec2-describe-spot-fleet-requests.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-spot-instance-requests.html
aws ec2 describe-spot-instance-requests > ec2-describe-spot-instance-requests.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-subnets.html
aws ec2 describe-subnets > ec2-describe-subnets.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-tags.html
aws ec2 describe-tags > ec2-describe-tags.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-volume-status.html
aws ec2 describe-volume-status > ec2-describe-volume-status.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-volumes.html
aws ec2 describe-volumes > ec2-describe-volumes.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-classic-link.html
aws ec2 describe-vpc-classic-link > ec2-describe-vpc-classic-link.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-classic-link-dns-support.html
aws ec2 describe-vpc-classic-link-dns-support > ec2-describe-vpc-classic-link-dns-support.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-endpoints.html
aws ec2 describe-vpc-endpoints > ec2-describe-vpc-endpoints.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpc-peering-connections.html
aws ec2 describe-vpc-peering-connections > ec2-describe-vpc-peering-connections.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpcs.html
aws ec2 describe-vpcs > ec2-describe-vpcs.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpn-connections.html
aws ec2 describe-vpn-connections > ec2-describe-vpn-connections.json
# https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpn-gateways.html
aws ec2 describe-vpn-gateways > ec2-describe-vpn-gateways.json

# https://docs.aws.amazon.com/cli/latest/reference/s3/ls.html
aws s3 ls > s3-list-buckets.txt

# https://docs.aws.amazon.com/cli/latest/reference/support/index.html
###
# https://docs.aws.amazon.com/cli/latest/reference/support/describe-cases.html
aws support describe-cases --include-resolved-cases > support-describe-cases.json

# https://docs.aws.amazon.com/cli/latest/reference/directconnect/index.html
###
# https://docs.aws.amazon.com/cli/latest/reference/directconnect/describe-connections.html
aws directconnect describe-connections > directconnect-describe-connections.json
# https://docs.aws.amazon.com/cli/latest/reference/directconnect/describe-interconnects.html
aws directconnect describe-interconnects > directconnect-describe-interconnects.json
# https://docs.aws.amazon.com/cli/latest/reference/directconnect/describe-virtual-gateways.html
aws directconnect describe-virtual-gateways > directconnect-describe-virtual-gateways.json
# https://docs.aws.amazon.com/cli/latest/reference/directconnect/describe-virtual-interfaces.html
aws directconnect describe-virtual-interfaces > directconnect-describe-virtual-interfaces.json

# https://docs.aws.amazon.com/cli/latest/reference/cloudtrail/index.html
###
# https://docs.aws.amazon.com/cli/latest/reference/cloudtrail/describe-trails.html
aws cloudtrail describe-trails > cloudtrail-describe-trails.json
# https://docs.aws.amazon.com/cli/latest/reference/cloudtrail/list-public-keys.html
aws cloudtrail list-public-keys > cloudtrail-list-public-keys.json

# https://docs.aws.amazon.com/cli/latest/reference/cloudformation/
###
# https://docs.aws.amazon.com/cli/latest/reference/cloudformation/describe-account-limits.html
aws cloudformation describe-account-limits > cloudformation-describe-account-limits.json
# https://docs.aws.amazon.com/cli/latest/reference/cloudformation/describe-stacks.html
aws cloudformation describe-stacks > cloudformation-describe-stacks.json
# https://docs.aws.amazon.com/cli/latest/reference/cloudformation/list-exports.html
aws cloudformation list-exports > cloudformation-list-exports.json
# https://docs.aws.amazon.com/cli/latest/reference/cloudformation/list-stacks.html
aws cloudformation list-stacks > cloudformation-list-stacks.json
















