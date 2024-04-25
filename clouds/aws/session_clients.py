import boto3
import botocore


def aws_session(**kwargs: str) -> boto3.session.Session:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.client
    return boto3.session.Session(**kwargs)


def iam_client(**kwargs) -> botocore.client.IAM:  # type: ignore
    return aws_session(**kwargs).client(service_name="iam")


def ec2_client(**kwargs) -> botocore.client.EC2:  # type: ignore
    return aws_session(**kwargs).client(service_name="ec2")


def s3_client(**kwargs) -> botocore.client.S3:  # type: ignore
    return aws_session(**kwargs).client(service_name="s3")


def rds_client(**kwargs) -> botocore.client.RDS:  # type: ignore
    return aws_session(**kwargs).client(service_name="rds")
