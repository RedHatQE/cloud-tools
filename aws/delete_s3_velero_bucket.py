"""
The main purpose of this script is to delete a bucket associated with a cluster
after the cluster is uninstalled:
-   The script will delete the velero bucket that is mapped to a cluster.

Required:
    AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY as environment variable or input argument
    cluster name as argument

Usage:
1. The module can be imported and used like below :

    import delete_s3_velero_bucket

    delete_s3_bucket.delete_velero_cluster_buckets(cluster)
    -   cluster: the name of the cluster

2.  python delete_s3_velero_bucket.py
        --aws_access_key_id=<access-key> --aws_secret_access_key=<secret> -c|--cluster <cluster_name>

"""
import json
import logging
import os
import re
import sys
from http import HTTPStatus
from typing import Union

import boto3
import click

LOGGER = logging.getLogger(__name__)


def delete_velero_cluster_buckets(cluster, boto_client) -> None:
    """
    Delete the velero bucket associated with a cluster

    Args:
        cluster: The cluster name
        boto_client: aws boto client


    """

    LOGGER.info(f"Delete velero buckets for '{cluster}' cluster")

    velero_bucket_list = get_velero_buckets(boto_client=boto_client)
    if not velero_bucket_list:
        LOGGER.info("No velero buckets found")
        return

    for bucket in velero_bucket_list:
        bucket_name = bucket["Name"]
        if verify_cluster_matches_velero_infrastructure_name(
            boto_client=boto_client,
            cluster_name=cluster,
            bucket_name=bucket_name,
        ):
            delete_all_objects_from_s3_folder(
                bucket_name=bucket_name, boto_client=boto_client
            )
            delete_bucket(bucket_name=bucket_name, boto_client=boto_client)
            # A cluster is mapped to only one bucket, so don't check any remaining buckets
            return

    LOGGER.info("No buckets deleted")


def delete_bucket(bucket_name: str, boto_client) -> None:
    """
    Delete velero bucket

    Args:
        bucket_name: the bucket name
        boto_client: AWS client
    """
    LOGGER.info(f"Delete bucket {bucket_name}")
    response = boto_client.delete_bucket(Bucket=bucket_name)

    response_http_status_code = response["ResponseMetadata"]["HTTPStatusCode"]
    if response_http_status_code == HTTPStatus.NO_CONTENT:
        LOGGER.info(f"Cluster bucket '{bucket_name}' deleted successfully")
        return

    elif response_http_status_code == HTTPStatus.NOT_FOUND:
        LOGGER.info(f"Bucket '{bucket_name}' not found")
        return

    LOGGER.error(
        f"Bucket {bucket_name} not deleted",
        json.dumps(response, defualt=str, indent=4),
    )
    sys.exit(1)


def get_velero_buckets(boto_client) -> list:
    """
    Get a list of velero buckets

    Args:
        boto_client: AWS client

    Returns:
        list of velero buckets
    """
    LOGGER.info("Get a list of velero buckets")

    buckets = boto_client.list_buckets()["Buckets"]
    return [
        bucket
        for bucket in buckets
        if re.search("managed-velero-backups-", bucket["Name"])
    ]


def get_velero_infrastructure_name(bucket_name: str, boto_client) -> Union[str, None]:
    """
    Get the velero bucket infrastructure name

    Args:
        bucket_name: The name of the cluster bucket to delete
        boto_client: AWS client

    Returns:
        str or None: velero infrastructure name if found else None
    """

    LOGGER.info(f"Get tags for bucket: {bucket_name}")
    bucket_tags = boto_client.get_bucket_tagging(Bucket=bucket_name)["TagSet"]

    for tag in bucket_tags:
        if tag["Key"] == "velero.io/infrastructureName":
            return tag["Value"]


def verify_cluster_matches_velero_infrastructure_name(
    boto_client,
    cluster_name: str,
    bucket_name: str,
) -> bool:
    """
    Get the velero bucket infrastructure name and compare it with the cluster

    Args:
        boto_client: AWS client
        cluster_name: The cluster name
        bucket_name: The bucket name

    Returns:
         bool: True if the cluster matches a velero infrastructure name, False otherwise
    """

    LOGGER.info(
        f"Verify cluster matches a velero infrastructure name via its bucket tag: {bucket_name}",
    )

    velero_infrastructure_name = get_velero_infrastructure_name(
        bucket_name=bucket_name, boto_client=boto_client
    )

    # Verify if the bucket is associated with the cluster
    if velero_infrastructure_name and re.search(
        rf"{cluster_name}(-\w+)?$",
        velero_infrastructure_name,
    ):
        LOGGER.info(
            f"Verified cluster '{cluster_name}' "
            f"is associated with velero infrastructure name {velero_infrastructure_name}",
        )
        return True

    return False


def delete_all_objects_from_s3_folder(bucket_name: str, boto_client) -> None:
    """
    Deletes all files in a folder of an S3 bucket

    Args:
        bucket_name: The bucket name
        boto_client: AWS client
    """

    list_obj_response = boto_client.list_objects_v2(Bucket=bucket_name)

    #  Sometimes there maybe no contents -- no objects
    files_in_folder = list_obj_response.get("Contents")
    if not files_in_folder:
        LOGGER.info(f"No objects to be deleted for {bucket_name}")
        return

    files_to_delete = [{"Key": file["Key"]} for file in files_in_folder]
    delete_response = boto_client.delete_objects(
        Bucket=bucket_name,
        Delete={"Objects": files_to_delete, "Quiet": True},
    )

    delete_response_http_status_code = delete_response["ResponseMetadata"][
        "HTTPStatusCode"
    ]
    if delete_response_http_status_code == HTTPStatus.OK:
        LOGGER.info("Objects deleted successfully")
        return
    else:
        LOGGER.error(
            "Objects not deleted:\n:"
            f"{json.dumps(delete_response, default=str, indent=4)}",
        )
        sys.exit(1)


@click.command()
@click.option(
    "--aws-access-key-id",
    help="Set AWS access key id, default if taken from environment variable: AWS_ACCESS_KEY_ID",
    required=True,
    default=os.getenv("AWS_ACCESS_KEY_ID"),
)
@click.option(
    "--aws-secret-access-key",
    help="Set AWS secret access key id,default if taken from environment variable: AWS_SECRET_ACCESS_KEY",
    required=True,
    default=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
@click.option(
    "-c",
    "--cluster-name",
    help="",
    required=True,
    default=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
def main(aws_access_key_id, aws_secret_access_key, cluster_name):
    boto_client = boto3.client(
        service_name="s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    delete_velero_cluster_buckets(cluster=cluster_name, boto_client=boto_client)


if __name__ == "__main__":
    main()
