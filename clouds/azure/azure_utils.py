import random
import string
from session_clients import get_resource_client, get_network_client, get_azure_credentials
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def random_resource_postfix(length=4):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def get_aro_supported_versions(aro_client=None, region=None):
    return [aro_version.version for aro_version in aro_client.open_shift_versions.list(location=region)]


def cleanup_azure_resources():
    credential = get_azure_credentials()
    resource_client = get_resource_client(credential=credential)
    network_client = get_network_client(credential=credential)

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
