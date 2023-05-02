import boto3
import botocore.errorfactory
import botocore.exceptions
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)

ROLE_NAME = "ManagedOpenShift-Support-Role"
POLICY_NAME = "rhoam-sre-support-policy"
JSON_FILE = "rhoam-sre-support-policy.json"


class IAMClient:
    def __init__(self, region="us-east-1"):
        """Default region is us-east-1 also when param region_name is not given"""
        LOGGER.info(f"Creating IAM client using region {region}.")
        self.iam_client = boto3.client(service_name="iam")

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
                self.iam_client.put_role_policy(
                    RoleName=role_name,
                    PolicyName=policy_name,
                    PolicyDocument=policy_doc,
                )
            except botocore.exceptions as exc:
                LOGGER.info(f"Failed with role policy creation:\n{exc}")

    def check_available_role_policy(self, role_name):
        """
        Finds role policy by given name, using boto3 list_roles_policies.

        Args:
            role_name (str): role policy name

        Returns:
            False if the request fails with botocore 'NoSuchEntity' exception.
             This is the only way to check existence since the list method raises if the role doesn't exist.
        """
        try:
            self.iam_client.list_role_policies(RoleName=role_name)
            LOGGER.info(f"Policy role {role_name} exists.")
            return True
        except botocore.errorfactory.ClientError:
            return False


def main():
    iam_client = IAMClient()
    iam_client.create_role_policy(
        role_name=ROLE_NAME, policy_name=POLICY_NAME, policy_json_path=JSON_FILE
    )


if __name__ == "__main__":
    main()
