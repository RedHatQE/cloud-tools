import botocore.errorfactory
from aws.aws_clients import IAMClient
from botocore.exceptions import BotoCoreError
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


class AWSRoles:
    def __init__(self, client: IAMClient):
        """
        Manages AWS roles and role-policies.

        Args:
            client (IAMClient): AWS roles managements expects an IAM client entity
        """
        self.client = client

    def create_role_policy(self, role_name, policy_name, policy_json_path):
        """
        Create the role policy with specific configuration.

        Args:
            role_name (str): role policy name
            policy_name (str): policy name
            policy_json_path (str): path to json file that holds the policy documents

        Raises:
            If POST request failed
        """
        LOGGER.info(f"Creating new role {role_name} for policy {policy_name}.")
        if not self.check_if_role_policy_exists(role_name=role_name):
            try:
                with open(policy_json_path, "r") as fd:
                    policy_doc = fd.read()
            except (FileNotFoundError, OSError):
                LOGGER.error(
                    "Json policy document couldn't load. Please validate file path."
                )
                raise
            try:
                self.client.put_role_policy(
                    role_name=role_name,
                    policy_name=policy_name,
                    policy_document=policy_doc,
                )
            except BotoCoreError as exc:
                LOGGER.error(f"Failed with role policy creation:\n{exc}")
                raise

    def check_if_role_policy_exists(self, role_name: str):
        """
        Finds role policy existence by given name.

        Args:
            role_name (str): role policy name

        Returns:
            bool: True if a policy role is found else False.
        """
        try:
            self.client.list_role_policies(role_name=role_name)
            LOGGER.info(f"Policy role {role_name} exists.")
            return True
        except botocore.errorfactory.ClientError:
            # Fails when role policy doesn't exist.
            return False
