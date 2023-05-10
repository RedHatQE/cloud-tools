import boto3
import botocore.errorfactory
from botocore.exceptions import BotoCoreError
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def iam_client(region="us-east-1"):
    """Creates an IAM client.

    Args:
        region (str): Region to use for session, a client is associated with a single region. Defaults to us-east-1.

    Returns:
        botocore.client.IAM: Service client instance.

    Raises:
        BotoCoreError: If Failed with creating an AWS client session request.
    """
    LOGGER.info(f"Creating IAM client using region {region}.")
    try:
        return boto3.client(service_name="iam", region_name=region)
    except BotoCoreError as exc:
        LOGGER.error(f"Failed to connect with AWS client.\n{exc}")
        raise


def create_or_update_role_policy(role_name, policy_name, policy_document_path):
    """
    Create a new policy role or update an existing one.

    Args:
        role_name (str): role policy name
        policy_name (str): policy name
        policy_document_path (str): path to Json file that holds the policy documents

    Raises:
        OSError: If file read failed
        BotoCoreError: If POST request failed
    """
    client = iam_client()
    if role_policy_exists_by_name(iam_client=client, role_name=role_name):
        LOGGER.info(f"Updating role by documented policy in {policy_document_path}.")
    else:
        LOGGER.info(f"Creating new role {role_name} for policy {policy_name}.")
    try:
        with open(policy_document_path, "r") as fd:
            policy_document = fd.read()
    except OSError:
        LOGGER.error(
            f"Json policy document couldn't load. Please validate file path: '{policy_document_path}'."
        )
        raise
    try:
        client.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=policy_document,
        )
    except BotoCoreError as exc:
        LOGGER.error(f"Failed with role policy management:\n{exc}")
        raise


def role_policy_exists_by_name(iam_client, role_name):
    """
    Finds role policy existence by given name.

    Args:
        iam_client (botocore.client.IAM): AWS client
        role_name (str): role policy name

    Returns:
        bool: True if a policy role is found else False.
    """
    try:
        iam_client.list_role_policies(RoleName=role_name)
        LOGGER.info(f"Policy role {role_name} exists.")
        return True
    except botocore.errorfactory.ClientError:
        # Fails when role policy doesn't exist.
        return False
