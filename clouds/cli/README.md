# Cloud nuke CLI tools
### AWS nuke
* Pre-requisites:
- Install `cloud-nuke` CLI tool (see https://github.com/gruntwork-io/cloud-nuke)
* Run nuke for specific AWS regions cloud resources:
```bash
poetry run python clouds/cli/aws_cli.py --aws-regions "us-east-1,us-west-2"
```
* Run nuke for all AWS regions:
```bash
poetry run python clouds/cli/aws_cli.py --all-aws-regions
```
### Azure nuke
* Run nuke for all Azure cloud resources that are associated with given credentials:
```bash
poetry run python clouds/cli/azure_cli.py \
              --azure-client-id=$AZURE_CLIENT_ID \
              --azure-tenant-id=$AZURE_TENANT_ID \
              --azure-client-secret=$AZURE_CLIENT_SECRET \
              --azure-subscription-id=$AZURE_SUBSCRIPTION_ID
```
