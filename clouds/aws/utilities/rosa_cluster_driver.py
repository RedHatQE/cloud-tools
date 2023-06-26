import os
from datetime import datetime, timedelta

from rosa.cli import execute
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def build_command_with_params(
    cluster_name,
    cluster_expiration,
    replicas,
    compute_machine_type,
    openshift_version,
    aws_region,
    channel_group,
):
    return (
        "create cluster "
        f"--cluster-name={cluster_name} "
        "--sts "
        f"--region={aws_region} "
        f"--channel-group={channel_group} "
        f"--version={openshift_version} "
        f"--expiration-time={cluster_expiration}Z "
        f"--replicas={replicas} "
        f"--compute-machine-type={compute_machine_type}"
    )


def main():
    ocm_token = "OCM_TOKEN"
    ocm_env_url = "ENV_URL"
    if not os.getenv(key=ocm_token) or not os.getenv(key=ocm_env_url):
        LOGGER.error(f"{ocm_token} and {ocm_env_url} env vars must be set.")
        exit(1)

    cluster_expiration = (
        datetime.now() + timedelta(hours=int(os.getenv("CLUSTER_TIME", "5")))
    ).isoformat()
    num_replicas = os.getenv(key="REPLICAS", default="2")
    compute_machine_type = os.getenv(key="INFRA_TYPE", default="m5.xlarge")
    cluster_name = os.getenv(key="CLUSTER_NAME", default="msi-rosa")
    openshift_version = os.getenv(key="OPENSHIFT_VERSION", default="4.13.3")
    aws_region = os.getenv(key="AWS_REGION", default="us-east-1")
    channel_group = os.getenv(key="CHANNEL", default="candidate")

    command = build_command_with_params(
        cluster_name=cluster_name,
        cluster_expiration=cluster_expiration,
        replicas=num_replicas,
        compute_machine_type=compute_machine_type,
        openshift_version=openshift_version,
        aws_region=aws_region,
        channel_group=channel_group,
    )

    std = execute(
        command=command, ocm_env=os.environ[ocm_env_url], token=os.environ[ocm_token]
    )

    LOGGER.err(f"stderr:\n{std['err']}")
    LOGGER.info(f"stdout:\n{std['out']}")


if __name__ == "__main__":
    main()
