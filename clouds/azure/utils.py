from typing import List
from simple_logger.logger import get_logger
from azure.core.exceptions import HttpResponseError
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.redhatopenshift import AzureRedHatOpenShiftClient

LOGGER = get_logger(name=__name__)


def get_aro_supported_versions(aro_client: AzureRedHatOpenShiftClient, region: str) -> List[str]:
    supported_versions = [aro_version.version for aro_version in aro_client.open_shift_versions.list(location=region)]
    LOGGER.info(f"ARO supported versions: {supported_versions}")
    return supported_versions


def get_azure_supported_regions(subscription_client: SubscriptionClient, subscription_id: str) -> List[str]:
    supported_regions = [
        region.name for region in subscription_client.subscriptions.list_locations(subscription_id=subscription_id)
    ]
    LOGGER.info(f"ARO supported regions: {supported_regions}")
    return supported_regions


def azure_resources_cleanup(resource_client: ResourceManagementClient) -> None:
    """
    Azure cloud resources are associated with resource groups.
    Running this cleanup function will destroy all existing leftover resources
    that are associated with the given resource client's subscription.
    Please note that this action is irreversible.
    Args:
        resource_client: Azure resources client (see https://learn.microsoft.com/en-us/python/api/azure-mgmt-resource/azure.mgmt.resource.resources.resourcemanagementclient?view=azure-python)
                            for more info.
    Returns:
        None
    """
    failed_delete_resource_groups = []
    azure_post_cleanup_message = "Azure cleanup completed successfully"

    LOGGER.info("Starting Azure resources cleanup")
    for resource_group_name in [resource_group.name for resource_group in resource_client.resource_groups.list()]:
        try:
            LOGGER.info(f"Deleting resource group {resource_group_name}")
            resource_client.resource_groups.begin_delete(resource_group_name=resource_group_name)
        except HttpResponseError as ex:
            LOGGER.error(f"Failed to delete resource group {resource_group_name}: {ex}")
            failed_delete_resource_groups.append(resource_group_name)

    if failed_delete_resource_groups:
        LOGGER.info(
            f"{azure_post_cleanup_message} except for the following resource groups: {failed_delete_resource_groups}"
        )
    else:
        LOGGER.info(f"{azure_post_cleanup_message}")
