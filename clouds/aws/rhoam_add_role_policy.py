import aws_clients
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)

ROLE_NAME = "ManagedOpenShift-Support-Role"
POLICY_NAME = "rhoam-sre-support-policy"
JSON_FILE = "rhoam-sre-support-policy.json"


def main():
    iam_client = aws_clients.IAMClient()
    iam_client.create_role_policy(
        role_name=ROLE_NAME, policy_name=POLICY_NAME, policy_json_path=JSON_FILE
    )


if __name__ == "__main__":
    main()
