import boto3
from botocore.exceptions import BotoCoreError
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


class AWSClient:
    def __init__(self, region="us-east-1", **kwargs):
        """Module for create an AWS client and manage its resources.

        Args:
            region (str): Region to use for session. Defaults to us-east-1.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            BotoCoreError: If Failed with creating an AWS client session request.
        """
        LOGGER.info(
            f"Creating {kwargs.get('service_name') or 'AWS'} client using region {region}."
        )
        try:
            self.client = boto3.client(region_name=region, **kwargs)
        except BotoCoreError as exc:
            LOGGER.error(f"Failed to connect with AWS client.\n{exc}")
            raise
