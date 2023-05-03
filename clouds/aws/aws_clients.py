import boto3
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


class AWSClient:
    def __init__(self, *args, **kwargs):
        """Default region is us-east-1 also when param region_name is not given"""
        region = kwargs.get("region") or "us-east-1"
        LOGGER.info(
            f"Creating {kwargs.get('service_name') or 'AWS'} client using region {region}."
        )
        try:
            self.client = boto3.client(*args, **kwargs)
        except Exception:
            LOGGER.info("Failed to connect with AWS client.")
            raise


class IAMClient(AWSClient):
    def __init__(self):
        super().__init__(service_name="iam")

    def list_role_policies(self, role_name):
        return self.client.list_role_policies(RoleName=role_name)

    def put_role_policy(self, role_name, policy_name, policy_document):
        return self.client.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=policy_document,
        )
