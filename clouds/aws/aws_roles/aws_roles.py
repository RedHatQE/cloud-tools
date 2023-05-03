import botocore.errorfactory
from aws.aws_clients import IAMClient
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


class AWSRolePolicies(AWSRoles):
    def __init__(self, client):
        super().__init__(client=client)

    def create_role_policy(self, role_name, policy_name, policy_json_path):
        """
        Create the role policy with specifications.

        Args:
            role_name (str): role policy name
            policy_name (str): policy name
            policy_json_path (str): path to json file that holds the policy documents

        Raises:
            If POST request failed
        """
        if not self.check_available_role_policy(role_name):
            LOGGER.info(f"Creating new role {role_name} for policy {policy_name}.")
            try:
                policy_doc = open(policy_json_path, "r").read()
            except Exception:
                LOGGER.info(
                    "Json policy document couldn't load. Please validate file path."
                )
                raise
            try:
                self.client.put_role_policy(
                    role_name=role_name,
                    policy_name=policy_name,
                    policy_document=policy_doc,
                )
                LOGGER.info("Done")
            except Exception as exc:
                LOGGER.info(f"Failed with role policy creation:\n{exc}")

    def check_available_role_policy(self, role_name=""):
        """
        Finds role policy by given name, using boto3 list_roles_policies.

        Args:
            role_name (str): role policy name

        Returns:
            False if the request fails with botocore 'NoSuchEntity' exception.
             This is the only way to check existence since the list method raises if the role doesn't exist.
        """
        try:
            self.client.list_role_policies(role_name=role_name)
            LOGGER.info(f"Policy role {role_name} exists.")
            return True
        except botocore.errorfactory.ClientError:
            # Fails when role policy doesn't exist.
            return False
