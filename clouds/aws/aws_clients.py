import boto3
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


class AWSClient:
    def __init__(self, *args, **kwargs):
        """Default region is us-east-1 also when param region_name is not given"""
        region = kwargs.get("region") or "us-east-1"
        LOGGER.info(f"Creating {kwargs.get('service_name') or 'AWS'} client using region {region}.")
        try:
            self.client = boto3.client(*args, **kwargs)
        except Exception:
            LOGGER.info("Failed to connect with AWS client.")
            raise


class IAMClient(AWSClient):
    def __init__(self):
        super().__init__(service_name="iam")

    def list_role_policies(self, RoleName):
        return self.client.list_role_policies(RoleName=RoleName)

    def put_role_policy(self, RoleName, PolicyName, PolicyDocument):
        return self.client.put_role_policy(
            RoleName=RoleName,
            PolicyName=PolicyName,
            PolicyDocument=PolicyDocument,
        )
