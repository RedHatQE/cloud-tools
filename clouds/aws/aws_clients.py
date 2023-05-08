import boto3
from botocore.exceptions import BotoCoreError
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


class AWSClient:
    def __init__(self, region="us-east-1", **kwargs):
        """Default region is us-east-1 also when param region_name is not given"""
        LOGGER.info(
            f"Creating {kwargs.get('service_name') or 'AWS'} client using region {region}."
        )
        try:
            self.client = boto3.client(region_name=region, **kwargs)
        except BotoCoreError as exc:
            LOGGER.error(f"Failed to connect with AWS client.\n{exc}")
            raise
