import aws_roles
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)

ROLE_NAME = "ManagedOpenShift-Support-Role"
POLICY_NAME = "rhoam-sre-support-policy"
JSON_FILE = "rhoam-sre-support-policy.json"


def main():
    aws_roles.create_or_update_role_policy(
        role_name=ROLE_NAME,
        policy_name=POLICY_NAME,
        policy_document_path=JSON_FILE,
    )


if __name__ == "__main__":
    main()
