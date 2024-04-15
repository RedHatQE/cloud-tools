from typing import List
from simple_logger.logger import get_logger
from azure.core.exceptions import HttpResponseError
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.redhatopenshift import AzureRedHatOpenShiftClient
from clouds.azure.session_clients import azure_credentials, resource_client


LOGGER = get_logger(name=__name__)


def get_aro_supported_versions(aro_client: AzureRedHatOpenShiftClient, region: str) -> List[str]:
    supported_versions: List[str] = [
        aro_version.version for aro_version in aro_client.open_shift_versions.list(location=region)
    ]
    LOGGER.info(f"ARO supported versions: {supported_versions}")
    return supported_versions


def get_azure_supported_regions(subscription_client: SubscriptionClient, subscription_id: str) -> List[str]:
    supported_regions: List[str] = [
        region.name for region in subscription_client.subscriptions.list_locations(subscription_id=subscription_id)
    ]
    LOGGER.info(f"ARO supported regions: {supported_regions}")
    return supported_regions


def nuke_all_azure_resources(tenant_id: str, client_id: str, client_secret: str, subscription_id: str) -> None:
    """
    Run nuke for all Azure cloud resources associated with the given credentials.

    Note:
        This action is irreversible and will permanently delete all resources.

    Args:
        tenant_id (str): The Azure managed-identity tenant ID.
        client_id (str): The Azure managed-identity client ID.
        client_secret (str): The Azure managed-identity client secret.
        subscription_id (str): The Azure subscription ID.
    """
    _resource_client = resource_client(
        credential=azure_credentials(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
        ),
        subscription_id=subscription_id,
    )

    failed_delete_resource_groups: List[str] = []
    azure_post_cleanup_message = "Azure cleanup completed"

    LOGGER.info("Starting Azure resources cleanup")
    for resource_group_name in [resource_group.name for resource_group in _resource_client.resource_groups.list()]:
        try:
            LOGGER.info(f"Deleting resource group {resource_group_name}")
            _resource_client.resource_groups.begin_delete(resource_group_name=resource_group_name)
        except HttpResponseError as ex:
            LOGGER.error(f"Failed to delete resource group {resource_group_name}: {ex}")
            failed_delete_resource_groups.append(resource_group_name)

    if failed_delete_resource_groups:
        LOGGER.info(
            f"{azure_post_cleanup_message} except for the following resource groups: {failed_delete_resource_groups}"
        )
    else:
        LOGGER.success(azure_post_cleanup_message)
