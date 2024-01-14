from session_clients import get_resource_client, get_network_client
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def cleanup_azure_resources():
    resource_client = get_resource_client()
    network_client = get_network_client()

    for resource_group_name in [resource_group.name for resource_group in resource_client.resource_groups.list()]:
        LOGGER.info(f"Deleting resources in {resource_group_name} resource group")
        for vnet_name in [
            vnet.name for vnet in network_client.virtual_networks.list(resource_group_name=resource_group_name)
        ]:
            network_client.virtual_networks.begin_delete(
                resource_group_name=resource_group_name,
                virtual_network_name=vnet_name,
            )
        LOGGER.info(f"Deleting {resource_group_name} resource group")
        resource_client.resource_groups.begin_delete(resource_group_name=resource_group_name)
    LOGGER.info("All Azure resources deleted successfully.")
