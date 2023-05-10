import boto3
from botocore.exceptions import BotoCoreError
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def aws_client(service_name, region="us-east-1", **kwargs):
    """Create an AWS client and manage its resources.

    Args:
        service_name (str): The name of a service, e.g. 's3' or 'ec2'.
        region (str): Region to use for session, a client is associated with a single region. Defaults to us-east-1.
        **kwargs (Any): Supported arguments to initialize a service client.
            - api_version (str): The API version to use.  By default, botocore will
                use the latest API version.
            - use_ssl (bool): Whether or not to use SSL. Defaulted to True.
                Note that not all services support non-ssl connections.
            - verify (bool): Whether to verify SSL certificates. Defaulted to True.
            - endpoint_url (str) : The complete URL to use for the constructed
                client. If this value is provided, then ``use_ssl`` is ignored
            - aws_access_key_id (str): The access key to use when creating
                the client.
            - aws_session_token (str): The session token to use when creating
                the client.
            - config (botocore.client.Config): Advanced client configuration options.

    Returns:
        Service client instance. (E.g. botocore.client.IAM)

    Raises:
        BotoCoreError: If Failed with creating an AWS client session request.
    """
    LOGGER.info(f"Creating {service_name} client using region {region}.")
    try:
        return boto3.client(service_name=service_name, region_name=region, **kwargs)
    except BotoCoreError as exc:
        LOGGER.error(f"Failed to connect with AWS client.\n{exc}")
        raise
