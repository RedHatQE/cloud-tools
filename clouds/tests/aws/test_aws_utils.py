from typing import Dict, List
from unittest.mock import patch

from clouds.aws.aws_utils import (
    set_and_verify_aws_credentials,
    set_and_verify_aws_config,
    delete_all_objects_from_s3_folder,
    delete_bucket,
    aws_region_names,
    get_least_crowded_aws_vpc_region,
)

os_environ_patch_str: str = "clouds.aws.aws_utils.os.environ"
config_parser_patch_str: str = "clouds.aws.aws_utils.ConfigParser"
ec2_client_patch_str: str = "clouds.aws.aws_utils.ec2_client"
botocore_client_patch_str: str = "clouds.aws.aws_utils.botocore.client"

dummy_bucket_name: str = "test_bucket"
us_east_region_str: str = "us-east-1"
us_west_region_str: str = "us-west-1"
default_aws_config_section: str = "default"


@patch(os_environ_patch_str)
@patch(config_parser_patch_str)
@patch(ec2_client_patch_str)
def test_set_and_verify_aws_credentials(mock_ec2_client, mock_config_parser, mock_os_environ, mocker):
    mock_os_environ.get.return_value = None

    mock_parser_instance = mocker.MagicMock()
    mock_config_parser.return_value = mock_parser_instance
    mock_parser_instance.get.side_effect = ["dummy_access_key", "dummy_secret_key"]

    mock_ec2_client_instance = mocker.MagicMock()
    mock_ec2_client.return_value = mock_ec2_client_instance
    mock_ec2_client_instance.describe_regions.return_value = {"Regions": [{"RegionName": us_east_region_str}]}

    set_and_verify_aws_credentials(region_name=us_east_region_str)

    mock_ec2_client.assert_called_once_with(region_name=us_east_region_str)
    mock_parser_instance.get.assert_any_call(default_aws_config_section, "aws_access_key_id")
    mock_parser_instance.get.assert_any_call(default_aws_config_section, "aws_secret_access_key")


@patch(os_environ_patch_str)
@patch(config_parser_patch_str)
def test_set_and_verify_aws_config(mock_config_parser, mock_os_environ, mocker):
    mock_os_environ.get.return_value = None

    mock_parser_instance = mocker.MagicMock()
    mock_config_parser.return_value = mock_parser_instance
    mock_parser_instance.get.return_value = us_east_region_str

    set_and_verify_aws_config()

    mock_parser_instance.get.assert_called_once_with(default_aws_config_section, "region")
    mock_os_environ.__setitem__.assert_called_once_with("AWS_REGION", us_east_region_str)  # noqa


@patch(botocore_client_patch_str)
def test_delete_all_objects_from_s3_folder(mock_s3_client, mocker):
    mock_boto_client = mocker.MagicMock()
    mock_s3_client.return_value = mock_boto_client

    s3_folder_objects_list: List[Dict[str, str]] = [{"Key": "file1"}, {"Key": "file2"}]

    mock_boto_client.list_objects_v2.return_value = {"Contents": s3_folder_objects_list}
    mock_boto_client.delete_objects.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}

    delete_all_objects_from_s3_folder(bucket_name=dummy_bucket_name, boto_client=mock_boto_client)

    mock_boto_client.list_objects_v2.assert_called_once_with(Bucket=dummy_bucket_name)
    mock_boto_client.delete_objects.assert_called_once_with(
        Bucket=dummy_bucket_name,
        Delete={"Objects": s3_folder_objects_list, "Quiet": True},
    )


@patch(botocore_client_patch_str)
def test_delete_bucket(mock_s3_client, mocker):
    mock_boto_client = mocker.MagicMock()
    mock_s3_client.return_value = mock_boto_client
    mock_boto_client.delete_bucket.return_value = {"ResponseMetadata": {"HTTPStatusCode": 204}}

    delete_bucket(bucket_name=dummy_bucket_name, boto_client=mock_boto_client)

    mock_boto_client.delete_bucket.assert_called_once_with(Bucket=dummy_bucket_name)


@patch(ec2_client_patch_str)
def test_aws_region_names(mock_ec2_client, mocker):
    mock_ec2_client_instance = mocker.MagicMock()
    mock_ec2_client.return_value = mock_ec2_client_instance
    mock_ec2_client_instance.describe_regions.return_value = {"Regions": [{"RegionName": us_east_region_str}]}

    regions = aws_region_names()

    assert regions == [us_east_region_str]
    mock_ec2_client_instance.describe_regions.assert_called_once()


@patch(ec2_client_patch_str)
def test_get_least_crowded_aws_vpc_region(mock_ec2_client, mocker):
    mock_ec2_client_instance_east = mocker.MagicMock()
    mock_ec2_client_instance_west = mocker.MagicMock()

    def mock_ec2_client_side_effect(region_name=None):
        if region_name == us_east_region_str:
            return mock_ec2_client_instance_east
        elif region_name == us_west_region_str:
            return mock_ec2_client_instance_west
        return None

    mock_ec2_client.side_effect = mock_ec2_client_side_effect

    mock_ec2_client_instance_east.describe_vpcs.return_value = {"Vpcs": ["vpc-1"]}
    mock_ec2_client_instance_west.describe_vpcs.return_value = {"Vpcs": ["vpc-2", "vpc-3"]}

    least_crowded_region = get_least_crowded_aws_vpc_region(region_list=[us_east_region_str, us_west_region_str])

    assert least_crowded_region == us_east_region_str
    mock_ec2_client_instance_east.describe_vpcs.assert_any_call()
    mock_ec2_client_instance_west.describe_vpcs.assert_any_call()
