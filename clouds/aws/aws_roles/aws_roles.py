import botocore.errorfactory
from aws.aws_clients import AWSClient
import boto3
from botocore.exceptions import BotoCoreError
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def get_iam_client():
    return AWSClient(service_name="iam").client


def create_role_policy(role_name, policy_name, policy_document_path, apply_update=False):
    """
    Create the role policy with specific configuration.

    Args:
        role_name (str): role policy name
        policy_name (str): policy name
        policy_document_path (str): path to Json file that holds the policy documents
        apply_update (bool): True to update the role policy if found, else False

    Raises:
        OSError: If file read failed
        BotoCoreError: If POST request failed
    """
    client = get_iam_client()
    LOGGER.info(f"Creating new role {role_name} for policy {policy_name}.")
    if apply_update or not check_if_role_policy_exists(iam_client=client, role_name=role_name):
        try:
            with open(policy_document_path, "r") as fd:
                policy_document = fd.read()
        except OSError:
            LOGGER.error(
                "Json policy document couldn't load. Please validate file path."
            )
            raise
        try:
            client.put_role_policy(
                RoleName=role_name,
                PolicyName=policy_name,
                PolicyDocument=policy_document,
            )
        except BotoCoreError as exc:
            LOGGER.error(f"Failed with role policy creation:\n{exc}")
            raise


def check_if_role_policy_exists(iam_client, role_name):
    """
    Finds role policy existence by given name.

    Args:
        iam_client (AWSClient): AWS client active session, expects an IAM client entity
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
